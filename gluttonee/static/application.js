(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  window.GT = {};
  GT.home = (function() {
    var centerImage, gHeight, gWidth, handleKeyPress, init, r, sX, sY, viewMainMenu, viewVenueDetails, viewVenueWheel;
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
      intervalHandler = null;
      keyEvent = function(e) {
        switch (e.which) {
          case 13:
            clearInterval(intervalHandler);
            viewVenueWheel().exec();
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
    viewVenueWheel = (__bind(function() {
      var addVenue, keyEvent, listVenues, randomImage, selectVenue, updateVenue, _this;
      _this = null;
      randomImage = function() {
        var img;
        img = centerImage('http://placekitten.com/100/100', Math.random(), Math.random(), 100, 100);
        return img.attr({
          opacity: '0.0'
        }).animate({
          opacity: '1.0'
        }, 2000);
      };
      listVenues = [];
      selectVenue = 0;
      addVenue = function(img) {
        return listVenues.push(img);
      };
      updateVenue = function() {
        var ele, idx, vlen, _len, _results;
        vlen = listVenues.length;
        _results = [];
        for (idx = 0, _len = listVenues.length; idx < _len; idx++) {
          ele = listVenues[idx];
          _results.push(ele.animate({
            x: sX(0.5 + 0.3 * Math.sin(2 * Math.PI * (idx - selectVenue) / vlen)),
            y: sY(0.5 - 0.3 * Math.cos(2 * Math.PI * (idx - selectVenue) / vlen)),
            easing: 'backOut'
          }, 500));
        }
        return _results;
      };
      keyEvent = function(e) {
        var ele, idx, vlen, _len;
        vlen = listVenues.length;
        switch (e.which) {
          case 37:
            selectVenue = (selectVenue + vlen - 1) % vlen;
            return updateVenue();
          case 39:
            selectVenue = (selectVenue + 1) % vlen;
            return updateVenue();
          case 13:
            for (idx = 0, _len = listVenues.length; idx < _len; idx++) {
              ele = listVenues[idx];
              if (idx !== selectVenue) {
                ele.stop().animate({
                  opacity: '0.0'
                }, 100);
              }
            }
            viewVenueDetails().exec(_this, listVenues[selectVenue]);
            eve.stop();
            return eve.unbind('key', keyEvent);
        }
      };
      return {
        restore: function() {
          var ele, _i, _len;
          eve.on('key', keyEvent);
          for (_i = 0, _len = listVenues.length; _i < _len; _i++) {
            ele = listVenues[_i];
            ele.stop().animate({
              opacity: '1.0'
            }, 100);
          }
          eve.on('key', keyEvent);
          return updateVenue();
        },
        exec: function() {
          _this = this;
          console.log(this);
          eve.on('key', keyEvent);
          addVenue(randomImage());
          addVenue(randomImage());
          addVenue(randomImage());
          addVenue(randomImage());
          addVenue(randomImage());
          addVenue(randomImage());
          addVenue(randomImage());
          return updateVenue();
        }
      };
    }, this));
    viewVenueDetails = (function() {
      var keyEvent, prevState;
      prevState = null;
      keyEvent = function(e) {
        switch (e.which) {
          case 27:
            eve.stop();
            eve.unbind('key', keyEvent);
            return prevState.restore();
          case 37:
            return null;
        }
      };
      return {
        exec: function(_prev, venue) {
          prevState = _prev;
          eve.on('key', keyEvent);
          return venue.animate({
            x: 0,
            y: 0,
            easing: 'backOut'
          }, 400);
        }
      };
    });
    init = function() {
      gWidth = document.body.clientWidth;
      gHeight = document.body.clientHeight;
      r = Raphael('canvas', '100%', '100%');
      $(document).keydown(function(e) {
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
