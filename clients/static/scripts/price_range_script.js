$(document).ready(function() {
  $("#price-range-submit").hide();
  min_price = localStorage.getItem("min_price_stadium");
  max_price = localStorage.getItem("max_price_stadium");
  if (min_price == null) {
    localStorage.setItem("min_price_stadium", 0);
  }
  if (max_price == null) {
    localStorage.setItem("max_price_stadium", 1000000);
  }
  $("#min_price_stadium,#max_price_stadium").on("change", function() {
    $("#price-range-submit").show();

    var min_price_range = parseInt($("#min_price_stadium").val());

    var max_price_range = parseInt($("#max_price_stadium").val());
    if (min_price_range > max_price_range) {
      $("#max_price_stadium").val(min_price_range);
    }

    $("#slider-range").slider({
      values: [min_price_range, max_price_range]
    });
  });

  $("#min_price_stadium,#max_price_stadium").on("paste keyup", function() {
    $("#price-range-submit").show();

    var min_price_range = parseInt($("#min_price_stadium").val());

    var max_price_range = parseInt($("#max_price_stadium").val());

    if (min_price_range == max_price_range) {
      max_price_range = min_price_range + 100;

      $("#min_price_stadium").val(min_price_range);
      $("#max_price_stadium").val(max_price_range);
    }

    $("#slider-range").slider({
      values: [min_price_range, max_price_range]
    });
  });

  $(function() {
    $("#slider-range").slider({
      range: true,
      orientation: "horizontal",
      min: 0,
      max: 1000000,
      values: [localStorage.getItem("min_price_stadium"), localStorage.getItem("max_price_stadium")],
      step: 100,

      slide: function(event, ui) {
        if (ui.values[0] == ui.values[1]) {
          return false;
        }
        $("#min_price_stadium").val(ui.values[0]);
        $("#max_price_stadium").val(ui.values[1]);

      },
    });

    $("#min_price_stadium").val($("#slider-range").slider("values", 0));
    $("#max_price_stadium").val($("#slider-range").slider("values", 1));
  });

  $("#slider-range,#submit-form-list").click(function() {
    var min_price_stadium = $("#min_price_stadium").val();
    var max_price_stadium = $("#max_price_stadium").val();

    localStorage.setItem("min_price_stadium", min_price_stadium);
    localStorage.setItem("max_price_stadium", max_price_stadium);
  });
});
