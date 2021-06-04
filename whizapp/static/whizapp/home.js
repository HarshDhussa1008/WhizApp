$(document).ready(function(){
      console.log('ready...')
      oTable=$('#posts').DataTable({"ordering": false,"lengthChange": false,"info":false,sDom: 'lrtip'});
      $('.dataTables_length').addClass('bs-select');
      $('#search').keyup(function(){
      oTable.search($(this).val()).draw() ;
      })
      $('table tr').click(function(){
        window.location = $(this).data('href');
        return false;
      });
});
