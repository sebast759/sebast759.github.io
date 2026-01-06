function csv_string_to_table(csv_string, element_to_insert_table) {
    var rows = csv_string.trim().split(/\r?\n|\r/); // Regex to split/separate the CSV rows
    var table = '';
    var table_rows = '';
    var table_header = '';

    rows.forEach(function(row, row_index) {
        var table_columns = '';
        var columns = row.split(','); // split/separate the columns in a row
        columns.forEach(function(column, column_index) {
            table_columns += row_index == 0 ? '<th>' + column + '</th>' : '<td>' + column + '</td>';
        });
        if (row_index == 0) {
            table_header += '<tr>' + table_columns + '</tr>';
        } else {
            table_rows += '<tr>' + table_columns + '</tr>';
        }
    });

    table += '<table>';
        table += '<thead>';
            table += table_header;
        table += '</thead>';
        table += '<tbody>';
            table += table_rows;
        table += '</tbody>';
    table += '</table>';

    element_to_insert_table.innerHTML += table;
}
 


