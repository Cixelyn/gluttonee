window.GT = {}
GT.home = ( ->

  gWidth = 0
  gHeight = 0
  r = null

  sX = (val) ->
    return val*gWidth

  sY = (val) ->
    return val*gHeight

  centerImage = (src,x,y,w,h) ->
    r.image(src,sX(x)-w/2,sY(y)-h/2,w,h)

  handleKeyPress = (e) ->
    switch e.which
      when 13 then this.click()
      when 27 then null # escape
      when 32 then null # space
      when 37 then this.left()
      when 38 then this.up()
      when 39 then this.right()
      when 40 then this.down()



  viewMainMenu = ( ->

    flickrData = null
    t_handle = null

    randomImage = () ->
      idx = Math.floor(Math.random()*flickrData.length)
      img = centerImage(flickrData[idx].media.m, Math.random(), Math.random(), 100, 100)
      img.attr({opacity: '0.0'}).animate {opacity: '1.0' }, 2000, ->
        img.animate {opacity: '0.0'}, 2000, ->
          img.remove()

    intervalHandler = null

    keyEvent = (e) ->
      switch e.which
        when 13
          t_handle.stop().animate {opacity: '0.0'}, 1000
          clearInterval(intervalHandler)
          viewVenueWheel().exec()
          eve.stop()
          eve.unbind('key', keyEvent)


    fontattr = {
      font: '70px "Nothing You Could Do"'
      fill: '#fff'
    }

    exec: () ->

      t_handle = r.text(gWidth/2,gHeight/2,'Gluttonee').attr(fontattr)


      # poll flickr
      $.getJSON("http://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?",
        {
          tags: "foodporn",
          tagmode: "any",
          format: "json"
        }, (data) ->
          flickrData = data.items
          intervalHandler = setInterval(randomImage, 1000)
          eve.on('key', keyEvent)
      )
  )


  viewVenueWheel = ( =>
    _this = null

    randomImage = () ->
      img = {}
      foodImgs = [
        'http://www.blogthingsimages.com/thepizzatest/pizza-9.jpg',
        'http://embedgames.ru/wp-content/thumbs/fast-food-car.jpg',
        'http://www.clipartguide.com/_thumbs/0511-1004-2020-3204.jpg',
        'http://www.free-clip-art.com/members/content/gallery/Food_Clip_Art/tn_Food084.jpg',
        'http://www.unclewaynes.net/images/BreadBowlCL.jpg',
        'http://images.meredith.com/bhg/images/07/s_pie.jpg',
        'http://www.blogthingsimages.com/whatkindofpieareyouquiz/pumpkin-pie.jpg']
      img.handle = centerImage(foodImgs[Math.floor(Math.random() * foodImgs.length)], Math.random(), Math.random(), 100, 100)
      img.handle.translate(-50, 0) .attr({opacity: '0.0'}).animate {opacity: '1.0' }, 2000
      return img

    listVenues = []
    selectVenue = 0
    lbl_name = null

    addVenue = (img) ->
      listVenues.push(img)

    updateVenue = () ->
      vlen = listVenues.length
      for ele,idx in listVenues
        ele.handle.animate {
          x: sX( 0.5 + 0.3 * Math.sin( 2*Math.PI * (idx-selectVenue) / vlen) ) - 50
          y: sY( 0.5 - 0.3 * Math.cos( 2*Math.PI * (idx-selectVenue) / vlen) )
          transform: if idx==selectVenue then 's1.5' else 's1'
          easing: 'backOut'
        }, 500
      lbl_name.attr('text',listVenues[selectVenue].ordin.na)

    keyEvent = (e) ->

      vlen = listVenues.length
      switch e.which
        when 37
          selectVenue = (selectVenue + vlen - 1) % vlen
          updateVenue()
        when 39
          selectVenue = (selectVenue + 1) % vlen
          updateVenue()
        when 13
          for ele,idx in listVenues
            if idx != selectVenue
              ele.handle.stop().animate {opacity:'0.0'},100

          viewVenueDetails().exec(_this,listVenues[selectVenue])

          eve.stop()
          eve.unbind('key', keyEvent)

    restore: () ->
      eve.on('key', keyEvent)
      for ven in listVenues
        ven.handle.stop().animate {opacity: '1.0'}, 100
      eve.on('key', keyEvent)
      updateVenue()


    exec: () ->
      _this = this
      console.log(this)
      eve.on('key', keyEvent)


      lbl_name = r.text(gWidth/2,60, '').attr {font: '40px "Nothing You Could Do"', fill: '#fff'}

      $.getJSON '/get_delivering_restaurants', null, (data) ->
        for info in data
          foodImgs = [
            'http://www.kitchenproject.com/pizza/images/Spaghettiand%20meatball%20pizza.jpg',
            'http://www.bigoven.com/pics/rs/256/pizza-unos-deep-pan-chicago-style-p.jpg',
            'http://www.bigoven.com/pics/rs/256/tuna-pasta-bake-3.jpg',
            'http://nimarcospizza.com/foodimgs/quad_pizza_tn.jpg',
            'http://www.bigoven.com/pics/rs/256/thai-grilled-pizza-4.jpg',
            'http://www.foodandbeverageunderground.com/image-files/san-miguel-de-allende-restaurants.jpg',
            'http://www.unclewaynes.net/images/BreadBowlCL.jpg',
            'http://images.meredith.com/bhg/images/07/s_pie.jpg',
            'http://www.bgfoods.com/bgcondiments/images/cuban_sandwich.jpg',
            'http://www.andysensei.com/blog/wp-images/pictures/Japan/China/chinaFood01.jpg',
            'http://files.blog-city.com/files/A06/59565224/p/f/chinese_food.jpg',
            'http://www.blogthingsimages.com/whatkindofpieareyouquiz/pumpkin-pie.jpg']
          handle = centerImage(foodImgs[Math.floor(Math.random() * foodImgs.length)], Math.random(), Math.random(), 100, 100)
          addVenue({
            ordin: info
            handle: handle
          })
          console.log(info)
          handle.attr({opacity: '0.0'}).animate {opacity: '1.0' }, 2000

        updateVenue()
  )

  viewVenueDetails = ( ->
    prevState = null
    entreesList = []
    selectIdx = 0

    keyEvent = (e) ->

      elen = entreesList.length
      switch e.which
        when 27 #escape
          eve.stop()
          eve.unbind('key', keyEvent)
          prevState.restore()
        when 38
          selectIdx = (selectIdx + elen - 1) % elen
          updateEntrees()
        when 39
          eve.stop()
          eve.unbind('key', keyEvent)
          prevState.restore()
        when 40
          selectIdx = (selectIdx + 1) % elen
          updateEntrees()

    updateEntrees = () ->
      for e,idx in entreesList
        e.handle.animate {
          x: sX(0.7)
          y: (idx - selectIdx) * 220
        }




    exec: (_prev,venue) ->
      prevState = _prev
      eve.on('key', keyEvent)
      venue.handle.animate {
        x: 0
        y: 0
        easing: 'backOut'
        transform: 's1'
      }, 400

      $.getJSON '/get_ordrin_data', {rID: venue.ordin.id}, (data) ->
        entrees =  _.flatten ( _.map data['menu'], (val) ->
          if val['children']? then val['children'] else val
        )

        for entree in entrees
          st = r.set()
          st.push(
            r.rect(0, 0, 400, 220, 10),
            r.text(400, 220, entree.name)
          )

          entreesList.push {
            details: entree
            handle: st
          }

        selectIdx = entrees.length
        updateEntrees()

  )


  init = ->
    # initialize Raphael.js
    gWidth = document.body.clientWidth
    gHeight = document.body.clientHeight
    r = Raphael('canvas', '100%', '100%')

    # bind keypress handler
    $(document).keydown (e) ->
      e.preventDefault()
      eve('key', null, e)

    # begin executing from the main menu
    viewMainMenu().exec()


  (
    init: init
  )

)()
