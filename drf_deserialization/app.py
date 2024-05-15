
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        .row {
            margin-top: 5px;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <form id="form">
        <div class="row">
            <input type="text" class="input" name="row1-col1">
            <input type="text" class="input" name="row1-col2">
            <span class="error" id="error1"></span>
        </div>
        <div class="row mt-2">
            <input type="text" class="input" name="row2-col1">
            <input type="text" class="input" name="row2-col2">
            <span class="error" id="error2"></span>
        </div>
        <div class="row mt-2">
            <input type="text" class="input" name="row3-col1">
            <input type="text" class="input" name="row3-col2">
            <span class="error" id="error3"></span>
        </div>
        <div class="row mt-2">
            <input type="text" class="input" name="row4-col1">
            <input type="text" class="input" name="row4-col2">
            <span class="error" id="error4"></span>
        </div>
        <button type="button" onclick="validateForm()">Submit</button>
    </form>

    <script>
        function validateInput(input, min, max) {
            const value = parseInt(input.value);
            return !isNaN(value) && value >= min && value <= max;
        }

        function validateForm() {
            let isValid = true;
            const ranges = [
                { min: 0, max: 100 },
                { min: 101, max: 200 },
                { min: 201, max: 300 },
                { min: 301, max: 400 }
            ];

            ranges.forEach((range, index) => {
                const row = index + 1;
                const input1 = document.querySelector(`input[name="row${row}-col1"]`);
                const input2 = document.querySelector(`input[name="row${row}-col2"]`);
                const error = document.getElementById(`error${row}`);

                if (!validateInput(input1, range.min, range.max) || !validateInput(input2, range.min, range.max)) {
                    error.textContent = `Values must be between ${range.min} and ${range.max}`;
                    isValid = false;
                } else {
                    error.textContent = '';
                }
            });

            if (isValid) {
                document.getElementById('form').submit();
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(template)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    errors = {}

    ranges = [
        (0, 100),
        (101, 200),
        (201, 300),
        (301, 400)
    ]

    for i, (min_val, max_val) in enumerate(ranges):
        row = i + 1
        col1 = f'row{row}-col1'
        col2 = f'row{row}-col2'
        try:
            val1 = int(data[col1])
            val2 = int(data[col2])
            if not (min_val <= val1 <= max_val) or not (min_val <= val2 <= max_val):
                errors[row] = f'Values must be between {min_val} and {max_val}'
        except ValueError:
            errors[row] = f'Invalid input in row {row}'

    if errors:
        return jsonify(errors=errors), 400
    return jsonify(message="Form submitted successfully"), 200

if __name__ == '__main__':
    app.run(debug=True)
