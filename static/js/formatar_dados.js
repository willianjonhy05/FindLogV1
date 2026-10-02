document.addEventListener('DOMContentLoaded', function () {
  // Função para formatar CNPJ: 00.000.000/0000-00
  function formatarCNPJ(cnpj) {
    let valor = cnpj.replace(/\D/g, '');
    if (valor.length !== 14) return cnpj; // Retorna o original se não tiver 14 dígitos
    return valor.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
  }

  // Função para formatar Telefone/Celular: (00) 0000-0000 ou (00) 00000-0000
  function formatarTelefone(telefone) {
    let valor = telefone.replace(/\D/g, '');
    
    if (valor.length === 11) {
      // Celular: (XX) XXXXX-XXXX
      return valor.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3');
    } else if (valor.length === 10) {
      // Fixo: (XX) XXXX-XXXX
      return valor.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
    }
    return telefone; // Retorna o original se não se enquadrar
  }

  // Aplica a formatação nos elementos que possuem a classe 'cnpj-format'
  document.querySelectorAll('.cnpj-format').forEach(function (td) {
    if (td.textContent) {
      td.textContent = formatarCNPJ(td.textContent.trim());
    }
  });

  // Aplica a formatação nos elementos que possuem a classe 'telefone-format'
  document.querySelectorAll('.telefone-format').forEach(function (td) {
    if (td.textContent) {
      td.textContent = formatarTelefone(td.textContent.trim());
    }
  });
});