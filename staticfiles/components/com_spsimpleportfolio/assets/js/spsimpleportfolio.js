/**
 * @package     SP Simple Portfolio
 *
 * @copyright   Copyright (C) 2010 - 2020 JoomShaper. All rights reserved.
 * @license     GNU General Public License version 2 or later.
 */
jQuery((function(e){e(window).on("load",(function(){var i=e(".sp-simpleportfolio-items"),s=i.find(".shuffle__sizer");i.shuffle({itemSelector:".sp-simpleportfolio-item",sequentialFadeDelay:150,sizer:s}),e(".sp-simpleportfolio-filter li a").on("click",(function(i){i.preventDefault();var s=e(this),l=e(this).parent();l.hasClass("active")||(s.closest("ul").children().removeClass("active"),s.parent().addClass("active"),s.closest(".sp-simpleportfolio").children(".sp-simpleportfolio-items").shuffle("shuffle",l.data("group")))}))}))}));