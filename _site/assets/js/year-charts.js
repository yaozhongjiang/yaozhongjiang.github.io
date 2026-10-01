(function () {
  var node = document.getElementById("yearly-data");
  if (!node) return;
  var data;
  try {
    data = JSON.parse(node.textContent);
  } catch (err) {
    return;
  }
  var charts = document.querySelectorAll(".year-chart");
  for (var c = 0; c < charts.length; c++) {
    draw(charts[c], data, charts[c].getAttribute("data-key"));
  }

  function draw(el, rows, key) {
    var w = 460;
    var h = 188;
    var pad = { l: 34, r: 12, t: 12, b: 52 };
    var nums = [];
    for (var i = 0; i < rows.length; i++) {
      var value = rows[i][key];
      if (value !== null && value !== undefined) nums.push(value);
    }
    var max = 1;
    for (var n = 0; n < nums.length; n++) {
      if (nums[n] > max) max = nums[n];
    }
    var count = rows.length;

    function x(index) {
      if (count <= 1) return pad.l;
      return pad.l + (index * (w - pad.l - pad.r)) / (count - 1);
    }
    function y(value) {
      return pad.t + (h - pad.t - pad.b) * (1 - value / max);
    }

    var parts = [];
    parts.push('<svg viewBox="0 0 ' + w + " " + h + '" role="img">');
    parts.push('<line x1="' + pad.l + '" y1="' + y(0) + '" x2="' + (w - pad.r) + '" y2="' + y(0) + '" stroke="#e6e7e8"/>');
    parts.push('<text x="' + (pad.l - 6) + '" y="' + (y(max) + 4) + '" text-anchor="end" font-size="11" fill="#7a8288">' + max + "</text>");
    parts.push('<text x="' + (pad.l - 6) + '" y="' + (y(0) + 4) + '" text-anchor="end" font-size="11" fill="#7a8288">0</text>');

    var points = [];
    var dots = [];
    for (var p = 0; p < rows.length; p++) {
      var row = rows[p];
      var point = row[key];
      if (point === null || point === undefined || point === "") point = 0;
      var px = x(p);
      var py = y(point);
      points.push(px + "," + py);
      dots.push('<circle cx="' + px + '" cy="' + py + '" r="3.2" fill="#224b8d"><title>' + row.year + ": " + point + "</title></circle>");
      parts.push('<text x="' + px + '" y="' + (h - 18) + '" text-anchor="end" font-size="10" fill="#7a8288" transform="rotate(-45 ' + px + " " + (h - 18) + ')">' + row.year + "</text>");
    }
    if (points.length > 1) {
      parts.push('<polyline fill="none" stroke="#224b8d" stroke-width="2" points="' + points.join(" ") + '"/>');
    }
    parts.push(dots.join(""));
    parts.push("</svg>");
    el.innerHTML = parts.join("");
  }
})();
