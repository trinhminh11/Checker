function heart_function(t, shrink_ratio = 2.5) {
    choice = random(1)
    if (choice < 0.5) {
        v1 = 1
        v2 = -1
    }
    else {
        v1 = -1
        v2 = -1
    }

    x = v1 * 0.1 * (-t * t + 40 * t + 1200) * sin(PI * t / 180)
    y = v2 * 0.1 * (-t * t + 40 * t + 1200) * cos(PI * t / 180) + 120 /2

    x *= shrink_ratio
    y *= shrink_ratio

    x += HEIGHT / 2
    y += WEIGHT / 2
    return [x, y]
}

function scatter_inside(x, y, beta = 0.15) {
    ratio_x = -beta * log(random(1))
    ratio_y = -beta * log(random(1))

    dx = ratio_x * (x - HEIGHT / 2)
    dy = ratio_y * (y - WEIGHT / 2)

    return [x - dx, y - dy]

}

function shrink(x, y, ratio) {
    force = -1 / (pow(pow(x - HEIGHT / 2, 2) + pow(y - WEIGHT / 2, 2), 0.6))
    dx = ratio * force * (x - HEIGHT / 2)
    dy = ratio * force * (y - WEIGHT / 2)
    return [x - dx, y - dy]
}

function curvee(p) {
    return 2 * (2 * sin(4 * p)) / (2 * PI)
}

function calc_position(x, y, ratio) {
    force = 1 / (pow(pow(x - HEIGHT / 2, 2) + pow(y - WEIGHT / 2, 2), 0.520))
    dx = ratio * force * (x - HEIGHT / 2) + int(random(-2, 2))
    dy = ratio * force * (y - WEIGHT / 2) + int(random(-2, 2))
    return [x - dx, y - dy]
}

function Heart() {
    generate_frame = 20
    this._points = new Set()
    this._edge_diffusion_points = new Set()
    this._center_diffusion_points = new Set()
    this.all_points = {}


    this.random_halo = 1000
    this.generate_frame = generate_frame



    this.build = function (number) {
        point_list = []
        for (var i = 0; i < number; i++) {
            t = random(0, 60)
            k = heart_function(t)
            this._points.add([k[0], k[1]])
        }
        point_list = Array.from(this._points)
        for (var i = 0; i < point_list.length; i++) {
            for (var j = 0; j < 3; j++) {
                k = scatter_inside(point_list[i][0], point_list[i][1], 0.05)
                this._edge_diffusion_points.add([k[0], k[1]])
            }

        }
        
        for (var i = 0; i < 4000; i++) {
            pointt = random(point_list)
            k = scatter_inside(pointt[0], pointt[1], 0.17)
            this._center_diffusion_points.add([k[0], k[1]])
        }
    }
    this.build(2000)

    this.calc = function (generate_frame1) {
        ratio = 10 * curvee(generate_frame1 / 10 * PI)
        halo_radius = int(4 + 6 * (1 + curvee(generate_frame1 / 10 * PI)))
        halo_number = int(3000 + 4000 * abs(pow(curvee(generate_frame1 / 10 * PI), 2)))

        all_points = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


        heart_halo_point = new Set()

        for (var i = 0; i <= halo_number; i++) {
            t = random(0, 60)
            k1 = heart_function(t, shrink_ratio = 2.6)
            k2 = shrink(k1[0], k1[1], halo_radius)
            x = k2[0]
            y = k2[1]
            if (heart_halo_point.has([x, y]) == false) {
                heart_halo_point.add([x, y])
                x += int(random(-15, 15))
                y += int(random(-15, 15))
                size = random([1, 2, 2])
                all_points.push([x, y, size])
            }
        }

        point_list = Array.from(this._points)
        for (var i = 0; i < point_list.length; i++) {
            k = calc_position(point_list[i][0], point_list[i][1], ratio)
            size = int(random(0, 4))
            all_points.push([k[0], k[1], size])
        }

        edgelist = Array.from(this._edge_diffusion_points)
        for (var i = 0; i < edgelist.length; i++) {
            k = calc_position(edgelist[i][0], edgelist[i][1], ratio)
            size = int(random(0, 3))
            all_points.push([k[0], k[1], size])
        }

        centerlist = Array.from(this._center_diffusion_points)
        for (var i = 0; i < centerlist.length; i++) {
            k = calc_position(centerlist[i][0], centerlist[i][1], ratio)
            size = int(random(0, 3))
            all_points.push([k[0], k[1], size])
        }

        this.all_points[generate_frame1] = all_points
    }

    for (var frame = 0; frame < this.generate_frame; frame++) {
        this.calc(frame)
    }

    this.show = function (render_frame) {
        for (var i = 0; i < this.all_points[render_frame % this.generate_frame].length; i++) {
           k = this.all_points[render_frame % this.generate_frame][i]
            strokeWeight(k[2])
            stroke('pink')
            point(k[0], k[1])
        }
    }

}
