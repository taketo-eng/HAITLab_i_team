'use strict';

(function($){

    $(()=>{
        //選択したファイルを表示するためのオブジェクト
        const file_name = $('#selected-file');
        //typeがfileであるオブジェクト
        const input = $('input[type=file]');
        //changeメソッドを使用
        input.change(function(){
            let file = $(this).prop('files')[0];
            file_name.text(file.name);
        });

        //gifを動かす
        let timestamp = new Date().getTime();
        $('#animation').attr('src', '../images/uploads/animation.gif' + '?' + timestamp);
    });

})(jQuery);