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

    intervalHandler = null

    randomImage = () ->
      img = centerImage('http://placekitten.com/100/100', Math.random(), Math.random(), 100, 100)
      img.attr({opacity: '0.0'}).animate {opacity: '1.0' }, 2000, ->
        img.animate {opacity: '0.0'}, 2000, ->
          img.remove()

    keyEvent = (e) ->
      console.log('triggered!')
      switch e.which
        when 13
          clearInterval(intervalHandler)
          viewSelectVenue().exec()
          eve.stop()
          eve.unbind('key', keyEvent)

    exec: () ->
      intervalHandler = setInterval(randomImage, 1000)
      eve.on('key', keyEvent)

  )



  viewSelectVenue = ( ->

    listVenues = []
    selectVenues = 0

    addVenue = (img) ->
      listVenues.push(img)

    keyEvent = (e) ->
      switch e.which
        when 37
          selectVenues = (selectVenues - 1) % listVenues.length
        when 39
          selectVenues = (selectVenues + 1) % listVenues.length


    exec: () ->
      eve.on('key', keyEvent)


  )






  init = ->
    # initialize Raphael.js
    gWidth = document.body.clientWidth
    gHeight = document.body.clientHeight
    r = Raphael('canvas', '100%', '100%')

    # bind keypress handler
    $(document).keypress (e) ->
      e.preventDefault()
      eve('key', null, e)

    # begin executing from the main menu
    viewMainMenu().exec()


  (
    init: init
  )

)()
