
$(document).ready(function() {

    $("header.navbar-fixed-top").autoHidingNavbar({
        showOnBottom: false
    });

    $('.show_hide').click(function() {
        $("#filters-content").slideToggle();
    });

    $('.dropdown-menu').find('form').click(function(e) {
        e.stopPropagation();
    });

    $.fn.dataTable.moment( 'DD-MM-YYYY HH:mm' );

    $('#data-table').DataTable({
        'pageLength': DATATABLE_PAGE_SIZE,
        'dom': "Bfrtip",
        fixedHeader: {
            header: true,
            footer: true
        },
        'buttons': [
            {   extend: 'excelHtml5',
                title: 'таблица',
                text: 'Экспортировать в Excel (.xlsx)'  },
            {   extend: 'print',
                title: '',
                text: 'распечатать'  },
            {   text: 'Добавить',
                    action: function (e, dt, node, config) {
                        $('#myModal').modal({ "show": true });
                        $('#save-btn').click(function(e) {
                             var me = $(this);
                             e.preventDefault();

                            if (me.data('requestRunning')) {
                                return;
                            }

                            me.data('requestRunning', true);
                            var form = $("#add-new-item");

                            $.ajax({
                                type: "POST",
                                url: form.attr("action"),
                                data: form.serialize(),
                                success: function(response) {
                                    console.log(response);
                                },
                                complete: function() {
                                    me.data('requestRunning', false);
                                }
                            });
                        });
                    } }
        ],
        'columnDefs': [
            { 'targets': "no-sort", orderable: false }     // 'targets' - указывает на имя css-класса для тегов <th> таблицы.
        ],
        'order': [[ 0, "desc" ]],                          // 'order' - задает номер колонки <th> (нумерация с нуля), по которой делается начальная default-сортировка
        'language': {
            'url': "https://cdn.datatables.net/plug-ins/1.10.13/i18n/Russian.json",
        }
    });

    var table = $('#data-table').DataTable();



    $(window).scroll(function() {
        var scrollh = $(this).scrollTop();
        if (scrollh == 0) {
            // $('.navbar').css({'height': '50px', });
            $('.navbar').removeClass("scrolled");
        }
        else {
            // $(".navbar").css({'height': '30px', });
            $('.navbar').addClass("scrolled");
        }

        if ($(this).scrollTop() > 50) {
            $('#back-to-top').fadeIn();
        } else {
            $('#back-to-top').fadeOut();
        }
    });

    // scroll body to 0px on click
    $('#back-to-top').click(function() {
        $('#back-to-top').tooltip('hide');
        $('body,html').animate({
            scrollTop: 0
        }, 800);
        return false;
    });

    $('#back-to-top').tooltip('show');


});

