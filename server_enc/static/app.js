const form = document.getElementById('form');
const submitButton = document.getElementById('submit-button');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  submitButton.disabled = true;
  send();
});

async function send() {
  weightElement = document.getElementById('weight');
  heightElement = document.getElementById('height');
  resultElement = document.getElementById('result');
  resultInnerElement = document.getElementById('result-inner');
  consoleInnerElement = document.getElementById('console-inner');

  const data = {
    weight: weightElement.value,
    height: heightElement.value
  };

  const response = await fetch('/calculate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
  });
  const result = await response.json();

  const consoleText = result['console'];
  const bmiValue = result['bmi'];
  const bmiClassification = getClassification(bmiValue);

  resultInnerElement.innerHTML = `
  <ul class="mb-0">
    <li>BMI: ${(result['bmi']).toFixed(2)}</li>
    <li>Classification: ${bmiClassification}</li>
  </ul>`;
  resultElement.style.display = 'block';
  consoleInnerElement.innerHTML = `<pre>${consoleText.trim()}</pre>
  `;

  submitButton.disabled = false;
}

function getClassification(bmi) {
  if (bmi < 16) return 'Severe Thinness';
  if (bmi >= 16 && bmi < 17) return 'Moderate Thinness';
  if (bmi >= 17 && bmi < 18.5) return 'Mild Thinness';
  if (bmi >= 18.5 && bmi < 25) return 'Normal';
  if (bmi >= 25 && bmi < 30) return 'Overweight';
  if (bmi >= 30 && bmi < 35) return 'Obese Class I';
  if (bmi >= 35 && bmi < 40) return 'Obese Class II';
  if (bmi >= 40) return 'Obese Class III';
}