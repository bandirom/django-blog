$('.toggler').click(function() {
    var tog = $(this);
    var secondDiv = tog.parent().prev();
    var firstDiv = secondDiv.prev();
    firstDiv.children('p').toggleClass('hide');
    secondDiv.toggleClass('hide');
    //tog.parent().find('.first > p').toggleClass('hide');
    //tog.parent().find('.second').toggleClass('hide');
    //$('.first > .main').toggleClass('hide');
    tog.toggleClass('fa fa-chevron-up fa fa-chevron-down');
    return false;
});

$('.comsys').click(function() {
    var togCmt = $(this);
    togCmt.toggleClass('active');
    var panelFooterDiv = togCmt.parent();
    var panelDefaultDiv = panelFooterDiv.parent();
    var panelCmtsDiv = panelDefaultDiv.next();
    panelCmtsDiv.slideToggle('hide');
    return false;
});
