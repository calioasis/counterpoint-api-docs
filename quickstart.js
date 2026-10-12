document.querySelectorAll('.copy').forEach(button => button.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(button.parentElement.querySelector('code').textContent);
    button.textContent = 'Copied';
  } catch (_) { button.textContent = 'Select text to copy'; }
  setTimeout(() => { button.textContent = 'Copy'; }, 2000);
}));
