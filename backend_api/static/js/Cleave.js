document.addEventListener('DOMContentLoaded', function () {
    new Cleave('#phone', {
        phone: true,
        phoneRegionCode: 'UA',  // Регион Украина
        prefix: '+38',          // Префикс для номера
        noImmediatePrefix: false,
        delimiter: ' ',
        blocks: [3, 3, 2, 2],   // Блоки цифр после кода
        numericOnly: true       // Только цифры
    });
});
