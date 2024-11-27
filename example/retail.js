const fs = require('fs');
const readlineSync = require('readline-sync');

// File to store the settings
const SETTINGS_FILE = 'settings_combined.json';

// Options
const modeOptions = ['Retail', 'Pay at Table'];
const errorOptions = ['Enable Declines', 'Enable Cancellations', 'Stop Response', 'None'];

// Initialize selections
let selectedRadio = 0; // Default selected radio option
let selectedErrorRadio = 3; // Default selected error option

// Amount details default values
const amountDetails = {
  Tip: '0.00',
  Cashback: '0.00',
  Surcharge: '0.00',
  Fee: '0.00',
};

// Default values
const features = {
  'Send Signature': false,
  'Currency Code': 'CAD',
  'Split Payment': false,
  'Split Amount': '0.00',
};

// Default credentials
const credentials = {
  TID: '',
  'Auth Key': '',
};

// Function to validate and format amount input
function validateAmountInput(inputStr) {
  const value = parseFloat(inputStr);
  return isNaN(value) ? null : value.toFixed(2);
}

// Function to validate the Currency Code (alphanumeric, 3 characters)
function validateCurrencyCode(inputStr) {
  if (/^[a-zA-Z0-9]{3}$/.test(inputStr)) {
    return inputStr.toUpperCase();
  }
  return null;
}

// Display options with selection
function displayMenu() {
  console.clear();
  console.log('NUVEI Terminal Simulator. Press Ctrl+C to quit.\n');

  // Mode selection
  console.log('Mode:');
  modeOptions.forEach((option, idx) => {
    console.log(`${selectedRadio === idx ? '(X)' : '( )'} ${option}`);
  });

  // Error options
  console.log('\nErrors/Declines:');
  errorOptions.forEach((option, idx) => {
    console.log(`${selectedErrorRadio === idx ? '(X)' : '( )'} ${option}`);
  });

  // Amount details
  console.log('\nAmount Details:');
  for (const [field, value] of Object.entries(amountDetails)) {
    console.log(`${field}: ${value}`);
  }

  // Features
  console.log('\nFeatures:');
  for (const [field, value] of Object.entries(features)) {
    if (typeof value === 'boolean') {
      console.log(`${value ? '[X]' : '[ ]'} ${field}`);
    } else {
      console.log(`${field}: ${value}`);
    }
  }

  // Credentials
  console.log('\nCredentials:');
  for (const [field, value] of Object.entries(credentials)) {
    console.log(`${field}: ${value}`);
  }
}

// Main loop for interaction
function main() {
  while (true) {
    displayMenu();

    // Get user choice
    const choice = readlineSync.question('\nSelect section (Mode, Errors, Amount, Features, Credentials): ').toLowerCase();

    switch (choice) {
      case 'mode':
        selectedRadio = readlineSync.keyInSelect(modeOptions, 'Choose a mode:');
        break;
      case 'errors':
        selectedErrorRadio = readlineSync.keyInSelect(errorOptions, 'Choose an error option:');
        break;
      case 'amount':
        const amountKey = readlineSync.keyInSelect(Object.keys(amountDetails), 'Select Amount Detail to edit:');
        if (amountKey !== -1) {
          const newValue = readlineSync.question('Enter new value: ');
          const validated = validateAmountInput(newValue);
          if (validated) amountDetails[Object.keys(amountDetails)[amountKey]] = validated;
        }
        break;
      case 'features':
        const featureKey = readlineSync.keyInSelect(Object.keys(features), 'Select Feature to edit:');
        if (featureKey !== -1) {
          const featureName = Object.keys(features)[featureKey];
          if (typeof features[featureName] === 'boolean') {
            features[featureName] = !features[featureName]; // Toggle checkbox
          } else if (featureName === 'Currency Code') {
            const newCode = readlineSync.question('Enter new currency code (3 characters): ');
            const validCode = validateCurrencyCode(newCode);
            if (validCode) features['Currency Code'] = validCode;
          } else if (featureName === 'Split Amount') {
            const newValue = readlineSync.question('Enter new split amount: ');
            const validated = validateAmountInput(newValue);
            if (validated) features['Split Amount'] = validated;
          }
        }
        break;
      case 'credentials':
        const credKey = readlineSync.keyInSelect(Object.keys(credentials), 'Select Credential to edit:');
        if (credKey !== -1) {
          const newValue = readlineSync.question(`Enter new value for ${Object.keys(credentials)[credKey]}: `);
          credentials[Object.keys(credentials)[credKey]] = newValue;
        }
        break;
      default:
        console.log('Invalid selection, please try again.');
    }

    // Save settings to file
    fs.writeFileSync(SETTINGS_FILE, JSON.stringify({ amountDetails, features, credentials }, null, 2));
    console.log('\nSettings saved!\n');
  }
}

// Run the main function
main();
