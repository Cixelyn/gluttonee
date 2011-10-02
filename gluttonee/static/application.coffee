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
          t_handle.stop().animate {opacity: '0.0'}, 1000, ->
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
          console.log(flickrData)
      )
  )


  viewVenueWheel = ( =>

    _this = null

    randomImage = () ->
      img = centerImage('http://placekitten.com/100/100', Math.random(), Math.random(), 100, 100)
      img.attr({opacity: '0.0'}).animate {opacity: '1.0' }, 2000

    listVenues = []
    selectVenue = 0

    addVenue = (img) ->
      listVenues.push(img)

    updateVenue = () ->
      vlen = listVenues.length
      for ele,idx in listVenues
        ele.animate {
          x: sX( 0.5 + 0.3 * Math.sin( 2*Math.PI * (idx-selectVenue) / vlen) )
          y: sY( 0.5 - 0.3 * Math.cos( 2*Math.PI * (idx-selectVenue) / vlen) )
          easing: 'backOut'
        }, 500

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
              ele.stop().animate {opacity:'0.0'},100

          viewVenueDetails().exec(_this,listVenues[selectVenue])

          eve.stop()
          eve.unbind('key', keyEvent)

    restore: () ->
      eve.on('key', keyEvent)
      for ele in listVenues
        ele.stop().animate {opacity: '1.0'}, 100
      eve.on('key', keyEvent)
      updateVenue()



    exec: () ->
      _this = this
      console.log(this)
      eve.on('key', keyEvent)
      addVenue(randomImage())
      addVenue(randomImage())
      addVenue(randomImage())
      addVenue(randomImage())
      addVenue(randomImage())
      addVenue(randomImage())
      addVenue(randomImage())
      updateVenue()
  )

  viewVenueDetails = ( ->
    prevState = null

    keyEvent = (e) ->
      switch e.which
        when 27 #escape
          eve.stop()
          eve.unbind('key', keyEvent)
          prevState.restore()
        when 37
          null
        when 38
          null
        when 40
          null

    exec: (_prev,venue) ->
      prevState = _prev
      eve.on('key', keyEvent)
      venue.animate {
        x: 0
        y: 0
        easing: 'backOut'
      }, 400
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
