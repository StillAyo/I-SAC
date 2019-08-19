
function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Full description:</td>'+
            '<td>Test</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Tags:</td>'+
            '<td>Test</td>'+
        '</tr>'
    
    '</table>';
}


// Initialize Pusher
    const pusher = new Pusher('2e0f7cfc70c03aaac02d', {
        cluster: 'eu',
        encrypted: true
    });

    // Subscribe to table channel
    var channel = pusher.subscribe('feed_check');

    channel.bind('new-feed', (data) => {


       // $('#table-div').append(`
       //      <tr id="${data.data.id} ">
       //          <th scope="row"> ${data.data.flight} </th>
       //          <td> ${data.data.destination} </td>
       //          <td> ${check_in} </td>
       //          <td> ${depature} </td>
       //          <td> ${data.data.status} </td>
       //      </tr>
       // `)
        var test = `${data.ids}`
        console.log(test);
        for (x of data.data) {

                $('#newEvent').append(`<br> <div class='col-sm-6'> 
                <div class='card' style='width: 75rem;'>
                <div class='card-body'>
                <h6 class='card-title'>New event</h6>
                <div class='table-wrapper' id='table-div'>
                <table class='table table-hover d' id='event'>
                <thead>
                <tr>
                <th style='width:7%'></th>
                <th style='width:6%'>ID</th>
                <th style='width:22%'>Description</th>
                <th style='width:20%'>Organisation</th>
                <th style='width:12%'>TLP</th>
                <th style='width:20%'>Category</th>
                <th style='width:13%'>Date</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                <td class='details-control'><p class='card-text'></p></td>
                <td scope='row'>${x.id}</td>
                <td><p class='card-text'>${x.eventName}</p></td>
                <td><p class='card-text'>${x.orgName}</p></td>
                <td><p class='card-text'>${x.tlp}</p></td>
                <td><p class='card-text'>${x.category}</p></td>
                <td><p class='card-text'>${x.date}</p></td>
                </tr>
                </tbody>
                </table>
                </div></div></div></div><br>`)

        }

    });

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
});
$(document).ready(function()
    var table = $('.d').DataTable({
        "paging":   false,
        "ordering": false,
        "info":     false
    });

    $("#searchInput").keyup(function () {
        // Filter on the column (the index) of this element
        table.fnFilterAll(this.value);
    });


    $('.d tbody').on('click', 'td.details-control', function () {
             var tr = $(this).closest('tr');
             var tdi = tr.find("i.fa");
             var row = table.row(tr);

             if (row.child.isShown()) {
                 // This row is already open - close it
                 row.child.hide();
                 tr.removeClass('shown');
                 tdi.first().removeClass('fa-minus-square');
                 tdi.first().addClass('fa-plus-square');
             }
             else {
                 // Open this row
                 row.child(format(row.data())).show();
                 tr.addClass('shown');
                 tdi.first().removeClass('fa-plus-square');
                 tdi.first().addClass('fa-minus-square');
             }
         });

         table.on("user-select", function (e, dt, type, cell, originalEvent) {
             if ($(cell.node()).hasClass("details-control")) {
                 e.preventDefault();
             }
         });

});






