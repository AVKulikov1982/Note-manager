 $(function ($) {
     $('#login').submit(function (e) {
         e.preventDefault()
         $.ajax({
             type: this.method,
             url: this.action,
             data: $(this).serialize(),
             dataType: 'json',
             success: function (response) {
                 console.log(response)
                 if (response.status === 200) {
                     window.location.replace("http://127.0.0.1:8000/")
                 }
             },
             error: function (response) {
                 console.log('err - ', response)
             }
         })
     })
 })