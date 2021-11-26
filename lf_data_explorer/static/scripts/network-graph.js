function update_variables(cy) {

    canvas_top = cy.extent()['y1']
    left = cy.extent()['x1']
    right = cy.extent()['x2']
    width = cy.extent()['w']
    height = cy.extent()['h']
    legend_scale = 0.2
    legend_left = right - width * legend_scale
    legend_spacing = height * 0.05
    font_size = height / 35
    line_width = height / 100
    line_padding = (font_size + line_width) / 2
}

function render_edge_legend(ctx) {
    update_variables(cy)

    ctx.lineWidth = line_width
    ctx.fillText("   Node Type", left + legend_spacing, canvas_top + legend_spacing);
    for (let i = 0; i < 3; i++) {
        ctx.fillStyle = "black"
        ctx.fillText(`${node_types[i]["name"]} Sample`, left + legend_spacing, canvas_top + legend_spacing * (i + 2));
        ctx.beginPath();
        ctx.strokeStyle = node_types[i]["colour"]
        ctx.fillStyle = node_types[i]["colour"]
        ctx.arc(left + legend_spacing + 0.15 * width, canvas_top + legend_spacing * (i + 2) - line_padding, 10, 0, 2 * Math.PI);
        ctx.stroke()
        ctx.fill()
    }
}

function render_node_legend(ctx) {

    ctx.fillStyle = "black"
    ctx.font = `${font_size}px Helvetica`;
    ctx.fillText("   Sample relationship", legend_left, canvas_top + legend_spacing);

    for (let i = 0; i < methods.length; i++) {
        ctx.strokeStyle = methods[i]["colour"];
        ctx.beginPath();
        ctx.moveTo(legend_left + width * 0.13, canvas_top + legend_spacing * (i + 2) - line_padding);
        ctx.lineTo(legend_left + width * 0.20, canvas_top + legend_spacing * (i + 2) - line_padding);
        ctx.closePath();
        ctx.stroke();
        ctx.fillText(methods[i]["name"], legend_left, canvas_top + legend_spacing * (i + 2));
    }
}

function clear_canvas(bottom_layer, ctx) {
    bottomLayer.resetTransform(ctx);
    bottomLayer.clear(ctx);
    bottomLayer.setTransform(ctx);
}