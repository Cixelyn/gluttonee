(function() {
  window.GT = {};
  GT.home = (function() {
    var centerImage, gHeight, gWidth, handleKeyPress, init, r, sX, sY, viewMainMenu, viewSelectVenue;
    gWidth = 0;
    gHeight = 0;
    r = null;
    sX = function(val) {
      return val * gWidth;
    };
    sY = function(val) {
      return val * gHeight;
    };
    centerImage = function(src, x, y, w, h) {
      return r.image(src, sX(x) - w / 2, sY(y) - h / 2, w, h);
    };
    handleKeyPress = function(e) {
      switch (e.which) {
        case 13:
          return this.click();
        case 27:
          return null;
        case 32:
          return null;
        case 37:
          return this.left();
        case 38:
          return this.up();
        case 39:
          return this.right();
        case 40:
          return this.down();
      }
    };
    viewMainMenu = (function() {
      var intervalHandler, keyEvent, randomImage;
      intervalHandler = null;
      randomImage = function() {
        var img;
        img = centerImage('http://placekitten.com/100/100', Math.random(), Math.random(), 100, 100);
        return img.attr({
          opacity: '0.0'
        }).animate({
          opacity: '1.0'
        }, 2000, function() {
          return img.animate({
            opacity: '0.0'
          }, 2000, function() {
            return img.remove();
          });
        });
      };
      keyEvent = function(e) {
        console.log('triggered!');
        switch (e.which) {
          case 13:
            clearInterval(intervalHandler);
            viewSelectVenue().exec();
            eve.stop();
            return eve.unbind('key', keyEvent);
        }
      };
      return {
        exec: function() {
          intervalHandler = setInterval(randomImage, 1000);
          return eve.on('key', keyEvent);
        }
      };
    });
    viewSelectVenue = (function() {
      var addVenue, keyEvent, listVenues, selectVenues;
      listVenues = [];
      selectVenues = 0;
      addVenue = function(img) {
        return listVenues.push(img);
      };
      keyEvent = function(e) {
        switch (e.which) {
          case 37:
            return selectVenues = (selectVenues - 1) % listVenues.length;
          case 39:
            return selectVenues = (selectVenues + 1) % listVenues.length;
        }
      };
      return {
        exec: function() {
          return eve.on('key', keyEvent);
        }
      };
    });
    init = function() {
      gWidth = document.body.clientWidth;
      gHeight = document.body.clientHeight;
      r = Raphael('canvas', '100%', '100%');
      $(document).keypress(function(e) {
        e.preventDefault();
        return eve('key', null, e);
      });
      return viewMainMenu().exec();
    };
    return {
      init: init
    };
  })();
}).call(this);
