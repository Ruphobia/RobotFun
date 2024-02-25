(module
  ;; Global variables for the dot's x and y positions, initialized away from edges to avoid immediate collision.
  (global $x (mut f32) (f32.const 50.0)) ;; Start away from the edge
  (global $y (mut f32) (f32.const 50.0)) ;; Start away from the edge

  ;; Global variables for the dot's velocity in x and y directions. Ensure movement in both directions.
  (global $dx (mut f32) (f32.const 2.0))
  (global $dy (mut f32) (f32.const 2.0))

  ;; Function to update the dot's position and handle bouncing.
  (func $updateAndBounce (export "updateAndBounce")
    (param $width f32)
    (param $height f32)
    
    ;; Update x position
    global.get $x
    global.get $dx
    f32.add
    global.set $x

    ;; Check for x boundary collision and adjust
    global.get $x
    f32.const 0.0
    f32.le
    if
      global.get $dx
      f32.neg
      global.set $dx
      f32.const 1.0
      global.set $x
    else
      global.get $x
      local.get $width
      f32.ge
      if
        global.get $dx
        f32.neg
        global.set $dx
        local.get $width
        f32.const 1.0
        f32.sub
        global.set $x
      end
    end

    ;; Update y position
    global.get $y
    global.get $dy
    f32.add
    global.set $y

    ;; Check for y boundary collision and adjust
    global.get $y
    f32.const 0.0
    f32.le
    if
      global.get $dy
      f32.neg
      global.set $dy
      f32.const 1.0
      global.set $y
    else
      global.get $y
      local.get $height
      f32.ge
      if
        global.get $dy
        f32.neg
        global.set $dy
        local.get $height
        f32.const 1.0
        f32.sub
        global.set $y
      end
    end
  )

  ;; Exported function to get the current x position.
  (func $getX (export "getX") (result f32)
    global.get $x
  )

  ;; Exported function to get the current y position.
  (func $getY (export "getY") (result f32)
    global.get $y
  )
)
