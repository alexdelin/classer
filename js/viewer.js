$("#addForm").bind('ajax:complete', function() {
         console.log('Done!')
});

console.log('Loaded')


$("#addSubmit").click(function() {
  console.log( "Handler for .click() called." );
});
