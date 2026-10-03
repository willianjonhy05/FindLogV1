document.addEventListener("DOMContentLoaded", function () {


    const botoesExcluir = document.querySelectorAll(".btn-delete");


    botoesExcluir.forEach(function (botao) {


        botao.addEventListener("click", function (event) {


            const nome = this.dataset.nome;


            const confirmar = confirm(
                `Deseja realmente excluir a instituição "${nome}"?`
            );


            if (!confirmar) {

                event.preventDefault();

            }


        });


    });


});