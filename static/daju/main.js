$(btn_template1).on("click", function () {
  $(template2).hide();
  $(template3).hide();
  $(template1).hide();
  $(template1).show(500);
});

$(btn_template2).on("click", function () {
  $(template1).hide();
  $(template3).hide();
  $(template2).hide();
  $(template2).show(500);
});

$(btn_template3).on("click", function () {
  $(template1).hide();
  $(template2).hide();
  $(template3).hide();
  $(template3).show(500);
});
