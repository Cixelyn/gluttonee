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
      var flickrData, fontattr, intervalHandler, keyEvent, randomImage, t_handle;
      flickrData = null;
      t_handle = null;
      randomImage = function() {
        var idx, img;
        idx = Math.floor(Math.random() * flickrData.length);
        img = centerImage(flickrData[idx].media.m, Math.random(), Math.random(), 100, 100);
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
            t_handle.stop().animate({
              opacity: '0.0'
            }, 1000);
            clearInterval(intervalHandler);
            viewVenueWheel().exec();
            eve.stop();
            return eve.unbind('key', keyEvent);
        }
      };
      fontattr = {
        font: '70px "Nothing You Could Do"',
        fill: '#fff'
      };
      return {
        exec: function() {
          t_handle = r.text(gWidth / 2, gHeight / 2, 'Gluttonee').attr(fontattr);
          return $.getJSON("http://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?", {
            tags: "foodporn",
            tagmode: "any",
            format: "json"
          }, function(data) {
            flickrData = data.items;
            intervalHandler = setInterval(randomImage, 1000);
            return eve.on('key', keyEvent);
          });
        }
      };
    });
    viewVenueWheel = (__bind(function() {
      var addVenue, keyEvent, lbl_name, listVenues, randomImage, selectVenue, updateVenue, _this;
      _this = null;
      randomImage = function() {
        var foodImgs, img;
        img = {};
        foodImgs = ['http://www.blogthingsimages.com/thepizzatest/pizza-9.jpg', 'http://embedgames.ru/wp-content/thumbs/fast-food-car.jpg', 'http://www.clipartguide.com/_thumbs/0511-1004-2020-3204.jpg', 'http://www.free-clip-art.com/members/content/gallery/Food_Clip_Art/tn_Food084.jpg', 'http://www.unclewaynes.net/images/BreadBowlCL.jpg', 'http://images.meredith.com/bhg/images/07/s_pie.jpg', 'http://www.blogthingsimages.com/whatkindofpieareyouquiz/pumpkin-pie.jpg'];
        img.handle = centerImage(foodImgs[Math.floor(Math.random() * foodImgs.length)], Math.random(), Math.random(), 100, 100);
        img.handle.translate(-50, 0).attr({
          opacity: '0.0'
        }).animate({
          opacity: '1.0'
        }, 2000);
        return img;
      };
      listVenues = [];
      selectVenue = 0;
      lbl_name = null;
      addVenue = function(img) {
        return listVenues.push(img);
      };
      updateVenue = function() {
        var ele, idx, vlen, _len;
        vlen = listVenues.length;
        for (idx = 0, _len = listVenues.length; idx < _len; idx++) {
          ele = listVenues[idx];
          ele.handle.animate({
            x: sX(0.5 + 0.3 * Math.sin(2 * Math.PI * (idx - selectVenue) / vlen)) - 50,
            y: sY(0.5 - 0.3 * Math.cos(2 * Math.PI * (idx - selectVenue) / vlen)),
            transform: idx === selectVenue ? 's1.5' : 's1',
            easing: 'backOut'
          }, 500);
        }
        return lbl_name.attr('text', listVenues[selectVenue].ordin.na);
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
                ele.handle.stop().animate({
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
          var ven, _i, _len;
          eve.on('key', keyEvent);
          for (_i = 0, _len = listVenues.length; _i < _len; _i++) {
            ven = listVenues[_i];
            ven.handle.stop().animate({
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
          lbl_name = r.text(gWidth / 2, 60, '').attr({
            font: '40px "Nothing You Could Do"',
            fill: '#fff'
          });
          return $.getJSON('/get_delivering_restaurants', null, function(data) {
            var foodImgs, handle, info, _i, _len;
            for (_i = 0, _len = data.length; _i < _len; _i++) {
              info = data[_i];
              foodImgs = ['http://www.kitchenproject.com/pizza/images/Spaghettiand%20meatball%20pizza.jpg', 'http://www.bigoven.com/pics/rs/256/pizza-unos-deep-pan-chicago-style-p.jpg', 'http://www.bigoven.com/pics/rs/256/tuna-pasta-bake-3.jpg', 'http://nimarcospizza.com/foodimgs/quad_pizza_tn.jpg', 'http://www.bigoven.com/pics/rs/256/thai-grilled-pizza-4.jpg', 'http://www.foodandbeverageunderground.com/image-files/san-miguel-de-allende-restaurants.jpg', 'http://www.unclewaynes.net/images/BreadBowlCL.jpg', 'http://images.meredith.com/bhg/images/07/s_pie.jpg', 'http://www.bgfoods.com/bgcondiments/images/cuban_sandwich.jpg', 'http://www.andysensei.com/blog/wp-images/pictures/Japan/China/chinaFood01.jpg', 'http://files.blog-city.com/files/A06/59565224/p/f/chinese_food.jpg', 'http://www.blogthingsimages.com/whatkindofpieareyouquiz/pumpkin-pie.jpg'];
              handle = centerImage(foodImgs[Math.floor(Math.random() * foodImgs.length)], Math.random(), Math.random(), 100, 100);
              addVenue({
                ordin: info,
                handle: handle
              });
              console.log(info);
              handle.attr({
                opacity: '0.0'
              }).animate({
                opacity: '1.0'
              }, 2000);
            }
            return updateVenue();
          });
        }
      };
    }, this));
    viewVenueDetails = (function() {
      var entreesList, keyEvent, prevState, selectIdx, updateEntrees;
      prevState = null;
      entreesList = [];
      selectIdx = 0;
      keyEvent = function(e) {
        var elen;
        elen = entreesList.length;
        switch (e.which) {
          case 27:
            eve.stop();
            eve.unbind('key', keyEvent);
            return prevState.restore();
          case 38:
            selectIdx = (selectIdx + elen - 1) % elen;
            return updateEntrees();
          case 39:
            eve.stop();
            eve.unbind('key', keyEvent);
            return prevState.restore();
          case 40:
            selectIdx = (selectIdx + 1) % elen;
            return updateEntrees();
        }
      };
      updateEntrees = function() {
        var e, idx, _len, _results;
        _results = [];
        for (idx = 0, _len = entreesList.length; idx < _len; idx++) {
          e = entreesList[idx];
          _results.push(e.handle.animate({
            x: sX(0.7),
            y: (idx - selectIdx) * 220
          }));
        }
        return _results;
      };
      return {
        exec: function(_prev, venue) {
          prevState = _prev;
          eve.on('key', keyEvent);
          venue.handle.animate({
            x: 0,
            y: 0,
            easing: 'backOut',
            transform: 's1'
          }, 400);
          return $.getJSON('/get_ordrin_data', {
            rID: venue.ordin.id
          }, function(data) {
            var entree, entrees, st, _i, _len;
            entrees = _.flatten(_.map(data['menu'], function(val) {
              if (val['children'] != null) {
                return val['children'];
              } else {
                return val;
              }
            }));
            for (_i = 0, _len = entrees.length; _i < _len; _i++) {
              entree = entrees[_i];
              st = r.set();
              st.push(r.rect(0, 0, 400, 220, 10), r.text(400, 220, entree.name));
              entreesList.push({
                details: entree,
                handle: st
              });
            }
            selectIdx = entrees.length;
            return updateEntrees();
          });
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
