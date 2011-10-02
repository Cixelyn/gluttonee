(function() {
  window.GT = {};
  GT.home = (function() {
    var showInit;
    showInit = function() {
      return 1 + 1;
    };
    return {
      showInit: showInit
    };
  })();
}).call(this);
