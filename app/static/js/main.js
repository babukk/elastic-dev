
$(document).ready(function() {
    /*
    $('.selectpicker').selectpicker({
        // style: 'btn-info',
        size: 12
    });
    */

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
                title: 'мониторинг',
                text: 'Экспортировать в Excel (.xlsx)'  },
            {   extend: 'print',
                title: 'Распечатать',
                text: 'Распечатать'  }
        ],
        'columnDefs': [
            { 'targets': "no-sort", orderable: false }     // 'targets' - указывает на имя css-класса для тегов <th> таблицы.
        ],
        'order': [[ 11, "desc" ]],                          // 'order' - задает номер колонки <th> (нумерация с нуля), по которой делается начальная default-сортировка
        'language': {
            'url': "https://cdn.datatables.net/plug-ins/1.10.13/i18n/Russian.json",
        }
    });

    var table = $('#data-table').DataTable();

    $(".clickable-row").click(function() {
        $("#data-table tbody tr").removeClass('row_selected');
        $(this).addClass('row_selected');

        var url = $(this).data("href");
        var ipaddr = $(this).data("ipaddr");
        $('#modal-body').load(url, function(result) {
            $('#myModal').modal({ "show": true });
            $('#save-comment-btn').click(function() {
                saveComment(ipaddr);
            });
        });
    });

    $('#myModal').on('hide.bs.modal', function () {
        $("#data-table tbody tr").removeClass('row_selected');
        // $.fn.dataTable.tables({visible: true, api: true}).columns.adjust();
    });

    $('#myModal').on('shown.bs.modal', function () {
        // waitingDialog.hide();
        // $.fn.dataTable.tables({visible: true, api: true}).columns.adjust();
    });

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

    $('.select2picker').select2();

});

