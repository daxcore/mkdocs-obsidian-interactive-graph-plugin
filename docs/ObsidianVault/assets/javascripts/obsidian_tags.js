$('.hash').each(function() {
  var link = $(this).html();
  $(this).contents().wrap('<a href="?q='+link+'">#</a>');
});
