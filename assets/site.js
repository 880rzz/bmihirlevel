(function () {
  var chips = Array.prototype.slice.call(document.querySelectorAll('[data-filter]'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('[data-cat]'));

  function apply(filter) {
    cards.forEach(function (card) {
      card.hidden = filter !== 'all' && card.getAttribute('data-cat') !== filter;
    });
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (other) {
        other.setAttribute('aria-pressed', String(other === chip));
      });
      apply(chip.getAttribute('data-filter'));
    });
  });

  var trigger = document.getElementById('josda-trigger');
  var panel = document.getElementById('josda-panel');
  var close = document.getElementById('josda-close');

  if (trigger && panel && close) {
    function setOpen(open) {
      panel.hidden = !open;
      trigger.setAttribute('aria-expanded', String(open));
      if (open) {
        close.focus();
      } else {
        trigger.focus();
      }
    }

    trigger.addEventListener('click', function () {
      setOpen(panel.hidden);
    });

    close.addEventListener('click', function () {
      setOpen(false);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !panel.hidden) {
        setOpen(false);
      }
    });

    document.addEventListener('click', function (event) {
      if (!panel.hidden && !panel.contains(event.target) && !trigger.contains(event.target)) {
        panel.hidden = true;
        trigger.setAttribute('aria-expanded', 'false');
      }
    });
  }
})();
