(function () {
  'use strict';

  var mathJaxSource = 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js';

  function ensureMathJax(previewWindow, previewDocument) {
    if (previewWindow.MathJax && previewWindow.MathJax.typesetPromise) {
      return Promise.resolve(previewWindow.MathJax);
    }

    if (previewWindow.lluviaMathJaxPromise) {
      return previewWindow.lluviaMathJaxPromise;
    }

    previewWindow.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']],
        processEscapes: true,
        tags: 'ams'
      },
      options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
      },
      startup: {
        typeset: false
      }
    };

    previewWindow.lluviaMathJaxPromise = new Promise(function (resolve, reject) {
      var script = previewDocument.createElement('script');
      script.src = mathJaxSource;
      script.async = true;
      script.dataset.lluviaMathJax = 'true';
      script.addEventListener('load', function () {
        Promise.resolve(previewWindow.MathJax.startup.promise).then(function () {
          resolve(previewWindow.MathJax);
        }, reject);
      });
      script.addEventListener('error', reject);
      previewDocument.head.appendChild(script);
    });

    return previewWindow.lluviaMathJaxPromise;
  }

  var LluviaPostPreview = createClass({
    componentDidMount: function () {
      this.queueTypeset();
    },

    componentDidUpdate: function () {
      this.queueTypeset();
    },

    componentWillUnmount: function () {
      this.previewRoot = null;
    },

    queueTypeset: function () {
      var component = this;
      var previewRoot = this.previewRoot;

      if (!previewRoot) {
        return;
      }

      if (this.props.entry.getIn(['data', 'mathjax']) === false) {
        if (this.props.window.MathJax && this.props.window.MathJax.typesetClear) {
          this.props.window.MathJax.typesetClear([previewRoot]);
        }
        return;
      }

      this.mathJaxQueue = (this.mathJaxQueue || Promise.resolve())
        .then(function () {
          return ensureMathJax(component.props.window, component.props.document);
        })
        .then(function (mathJax) {
          if (!component.previewRoot || !component.previewRoot.isConnected) {
            return undefined;
          }
          mathJax.typesetClear([component.previewRoot]);
          return mathJax.typesetPromise([component.previewRoot]);
        })
        .catch(function () {
          return undefined;
        });
    },

    render: function () {
      var component = this;
      var title = this.props.entry.getIn(['data', 'title']) || '文章预览';
      var subtitle = this.props.entry.getIn(['data', 'subtitle']);

      return h(
        'article',
        {
          className: 'lluvia-cms-preview',
          ref: function (node) {
            component.previewRoot = node;
          }
        },
        h(
          'header',
          { className: 'lluvia-cms-preview-header' },
          h('h1', {}, title),
          subtitle ? h('p', {}, subtitle) : null
        ),
        h('div', { className: 'post-container lluvia-cms-preview-body' }, this.props.widgetFor('body'))
      );
    }
  });

  CMS.registerPreviewStyle('/admin/preview.css');
  CMS.registerPreviewTemplate('posts', LluviaPostPreview);
  document.documentElement.dataset.lluviaMathPreview = 'registered';
  window.lluviaMathPreviewReady = true;
})();
