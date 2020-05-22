function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

$(function() {

    var $gdesg_table = ""
    var $gdesg_table_area = ""
    var $desg_table = ""
    var $desg_table_area = ""
    var create_desg_table_company = ""
    var $sect_table = ""
    var $current_row_table1 = ""
    var $current_row_table2 = ""
    var $current_sel_unit = null
    var $current_sel_unit_obj = {}
    var $desg_list = []
    var $desg_list_dict = {}
    //var $d5_list =[]
    var $d5_list_dict = {}
    var $sect_list = []
    var $sect_list_dict = {}

    var $add_gdesg_combo = null
    var $add_gdesg_data = null

    function get_static_json_results() {
        $.ajax('/assessment/get_all_desg/?', // request url
            {
                dataType: 'json', // type of response data
                timeout: 5000, // timeout milliseconds
                success: function(data, status, xhr) {
                    $desg_list = data
                    $desg_list.forEach(function(item) {
                        $desg_list_dict[item.d_code] = item
                        var $d5 = item.d_code.slice(-5)
                        if (!$d5_list_dict[$d5]) {
                            $d5_list_dict[$d5] = {
                                "d5": $d5,
                                "d_gdesig": item.d_gdesig,
                                "sample_dscd_code": item.d_code,
                                "d_year_id": item.d_year_id,
                                "d_id": item.d_id
                            }
                        }
                    })
                    //                            console.log($desg_list_dict)
                    //                            console.log($d5_list_dict)
                },
                error: function(jqXhr, textStatus, errorMessage) {
                    console.log("failed to retrieve desg data")
                }
            });
        $.ajax('/assessment/get_all_sect/?', {
            dataType: 'json', // type of response data
            timeout: 5000, // timeout milliseconds
            success: function(data, status, xhr) {
                $sect_list = data
                $sect_list.forEach(function(item) {
                    $sect_list_dict[item.s_code] = item
                })
                //                            console.log($sect_list_dict)
            },
            error: function(jqXhr, textStatus, errorMessage) {
                console.log("failed to retrieve sect data")
            }
        });

    }

    //alert();
    function get_stat(data) {
        $.ajax('/assessment/get_stat_for_gdesg_list?u_id=' + data.u_id + '&d5=' + data.d5 + '&a_order=' + data.a_order + '&u_type=' + data.u_type, // request url
            {
                dataType: 'json', // type of response data
                timeout: 5000, // timeout milliseconds
                success: function($data, status, xhr) {
                    //                            console.log($data)
                    $('#stat_gdesg').replaceWith($data);
                },
                error: function(jqXhr, textStatus, errorMessage) { // error callback
                    //        $('p').append('Error: ' + errorMessage);\
                    console.log(errorMessage)
                }
            });
    }

    function create_gdesg_table() {
        var table_1 = new Tabulator("#gdesg_table_area", {
            height: 300,
            layout: "fitColumns",
            tooltips: true, //show tool tips on cells
            addRowPos: "bottom", //when adding a new row, add it to the top of the table
            history: false, //allow undo and redo actions on the table
            //	pagination:"local",       //paginate the data
            //	paginationSize:7,         //allow 7 rows per page of data
            columnCalcs: "both",
            movableColumns: false, //allow column order to be changed
            resizableRows: false, //allow row order to be changed
            headerSort: false,
            placeholder: "No Data Available",
            //             footerElement:"<button>Custom Button</button>",
            initialSort: [ //set the initial sort order of the data
                {
                    column: "d_rank",
                    dir: "asc"
                },
            ],
            columns: [ //define the table columns
                {
                    title: "Area",
                    field: "a_name",
                    width: 100,
                    //                    headerFilter: "input"
                },
                {
                    title: "Group Desig",
                    field: "d_gdesig",
                    width: 150,
                    //                    headerFilter: "input"
                },
                //                {
                //                    title: "Code",
                //                    field: "d5",
                //                    align: "left",
                //                    width:100,
                //                    headerFilter: "input"
                //                },
                {
                    title: "rank",
                    field: "d_rank",
                    visible: false
                },
                {
                    title: "d_id",
                    field: "d_id",
                    visible: false
                },
                {
                    title: "u_id",
                    field: "u_id",
                    visible: false
                },
                {
                    title: "Prev San",
                    field: "psan",
                    align: "right",
                    width: 75,
                    bottomCalc: "sum",
                    //                     color:"green"
                },
                {
                    title: "Ext",
                    field: "ftot",
                    bottomCalc: "sum",
                    width: 75,
                    align: "right",
                    formatter: function(cell, formatterParams, onRendered) {
                        // console.log(cell)
                        var data = cell.getData()
                        //                        x=cell
                        var url = '<a class="light_link_column" target="_blank"  href="/assessment/emp/list/?e_unit_roll__u_id=' + data.u_id.slice(-6) + '&e_desg__d_id=' + data.d5.slice(-7) + '">' + cell.getValue() + '</a>'
                        //                        return cell.getValue().slice(-7);
                        return url
                    },
                },
                {
                    title: "Ret",
                    field: "retr0",
                    align: "right",
                    width: 75,
                    bottomCalc: "sum",
                },
                {
                    title: "Req",
                    field: "freq",
                    width: 75,
                    bottomCalc: "sum",
                    align: "right",
                    color: "orange"
                },
                {
                    title: "San",
                    field: "fsan",
                    align: "right",
                    width: 75,
                    bottomCalc: "sum",
                    color: "green"
                }
            ],
            rowClick: function(e, row) {
                //e - the click event object
                //row - row component
                $current_row_table1 = row
                var data = row.getData()
                //                console.log(data)
                //                $gdesg_table.setHeaderFilterValue("a_order", data.a_order);
                $gdesg_table.setFilter([{
                        field: "a_order",
                        type: "=",
                        value: data.a_order
                    },
                    {
                        field: "d5",
                        type: "=",
                        value: data.d5
                    }
                ]);
                load_desg_summary_area(filter_val, data.a_order)
            },
        });

        var table_2 = new Tabulator("#gdesg_table", {
            height: 300,
            layout: "fitColumns",
            tooltips: true, //show tool tips on cells
            addRowPos: "bottom", //when adding a new row, add it to the top of the table
            history: false, //allow undo and redo actions on the table
            //	pagination:"local",       //paginate the data
            //	paginationSize:7,         //allow 7 rows per page of data
            columnCalcs: "both",
            movableColumns: false, //allow column order to be changed
            resizableRows: false, //allow row order to be changed
            headerSort: false,
            //            groupClosedShowCalcs:true,
            //            groupBy:["a_name"],
            placeholder: "No Data Available",
            //             footerElement:"<button>Custom Button</button>",
            initialSort: [ //set the initial sort order of the data
                {
                    column: "d_rank",
                    dir: "asc"
                },
            ],
            columns: [ //define the table columns
                {
                    title: "Unit",
                    field: "u_name",
                    width: 100,
                    headerFilter: "input"
                },
                {
                    title: "Group Desig",
                    field: "d_gdesig",
                    width: 150,
                    headerFilter: "input"
                },
                //                {
                //                    title: "Code",
                //                    field: "d5",
                //                    align: "left",
                //                    width:100,
                //                    headerFilter: "input"
                //                },
                {
                    title: "rank",
                    field: "d_rank",
                    visible: false
                },
                {
                    title: "d_id",
                    field: "d_id",
                    visible: false
                },
                {
                    title: "u_id",
                    field: "u_id",
                    visible: false
                },
                {
                    title: "Prev San",
                    field: "psan",
                    align: "right",
                    width: 75,
                    bottomCalc: "sum",
                    //                     color:"green"
                },
                {
                    title: "Ext",
                    field: "ftot",
                    bottomCalc: "sum",
                    width: 75,
                    align: "right",
                    formatter: function(cell, formatterParams, onRendered) {
                        // console.log(cell)
                        var data = cell.getData()
                        //                        x=cell
                        var url = '<a class="light_link_column" target="_blank"  href="/assessment/emp/list/?e_unit_roll__u_id=' + data.u_id.slice(-6) + '&e_desg__d_id=' + data.d5.slice(-7) + '">' + cell.getValue() + '</a>'
                        //                        return cell.getValue().slice(-7);
                        return url
                    },
                },
                {
                    title: "Ret",
                    field: "retr0",
                    align: "right",
                    width: 75,
                    bottomCalc: "sum",
                },
                {
                    title: "Req",
                    field: "freq",
                    width: 75,
                    bottomCalc: "sum",
                    align: "right",
                    color: "orange"
                },
                {
                    title: "San",
                    field: "fsan",
                    align: "right",
                    width: 75,
                    bottomCalc: "sum",
                    color: "green"
                }
            ],
            rowClick: function(e, row) {
                //e - the click event object
                //row - row component
                $current_row_table2 = row
                var data = row.getData()
                //                console.log(data)
                $.ajax('/assessment/get_req_unit_desg?u_id=' + data.u_id + '&d5=' + data.d5, // request url
                    {
                        dataType: 'json', // type of response data
                        timeout: 5000, // timeout milliseconds
                        success: function($data, status, xhr) {
//                            console.log(data)
                            $desg_table.setData($data);
                            ($("#unit_header")[0]).textContent=(data.u_name)+" / "+data.a_name
                        },
                        error: function(jqXhr, textStatus, errorMessage) { // error callback
                            //        $('p').append('Error: ' + errorMessage);\
                            console.log(errorMessage)
                        }
                    });
                get_stat(data)
                //                $.ajax('/assessment/get_req_unit_sect?u_id=' + data.u_id + '&d5=' + data.d5, // request url
                //                    {
                //                        dataType: 'json', // type of response data
                //                        timeout: 5000, // timeout milliseconds
                //                        success: function($data, status, xhr) {
                ////                            console.log(data)
                //                            $sect_table.setData($data);
                //                        },
                //                        error: function(jqXhr, textStatus, errorMessage) { // error callback
                //                            //        $('p').append('Error: ' + errorMessage);
                //                        }
                //                    });
            },
        });

        return [table_1, table_2]
    }

    function add_d5_entry(value, text, $choice) {
        console.log(value, $current_sel_unit)
        if (value === "" || value === null)
            return null;
        var $d5 = $d5_list_dict[value]

        $.ajax('/assessment/get_unit_detail?u_id=' + $current_sel_unit, // request url
            {
                dataType: 'json', // type of response data
                timeout: 5000, // timeout milliseconds
                success: function(unit_detail, status, xhr) {
                    console.log(unit_detail)
                    var $data = {
                        "d5": value,
                        "d_id": $d5.d_id,
                        "u_name":unit_detail.u_name,
                        "u_type":unit_detail.u_type,
                        "a_name":unit_detail.u_area__a_name,
                        "a_order":unit_detail.u_area__a_order,
                        "u_id": $current_sel_unit,
                        "tot": 0,
                        "req": 0,
                        "san": 0,
                        "ftot": 0,
                        "freq": 0,
                        "fsan": 0,
                        "d_gdesig": $d5.d_gdesig,
                        "comment": ""
                    }
                    update_sanc_table($data)
                    $gdesg_table.addRow($data)
                        .then(function(row) {
                            $add_gdesg_combo.dropdown("clear");
                            $('[data-value=' + value + ']').remove()
                            //    $add_gdesg_combo.dropdown("remove selected",value)
                        }).catch(function(error) {
                            alert("Error: cannot add row")
                        });
                },
                error: function(jqXhr, textStatus, errorMessage) { // error callback
                    //        $('p').append('Error: ' + errorMessage);\
                    console.log(errorMessage)
                }
            });

    }

    function unit_load_new_entry(value, text, $choice) {
        console.log(value);
        $current_sel_unit = value
        $.ajax('/assessment/get_req_unit_gdesg?u_id=' + value, // request url
            {
                dataType: 'json', // type of response data
                timeout: 5000, // timeout milliseconds
                success: function(data, status, xhr) {
                    console.log(data)
                    //                    $gdesg_table.setData(data.unit_sanc );
                    //                    $desg_table.clearData();
                    //                    $sect_table.clearData();
                    $add_gdesg_combo = $('#add_gdesg').dropdown({
                        values: data.desg_list,
                        placeholder: "Insert new designation",
                        onChange: add_d5_entry
                    });
                    $add_gdesg_data = data.desg_list
                },
                error: function(jqXhr, textStatus, errorMessage) { // error callback
                    //        $('p').append('Error: ' + errorMessage);
                }
            });
    }

    $('#unit_select_for_new_entry').dropdown({
        onChange: unit_load_new_entry
    });

    //    $('#unit_select').dropdown({
    //        onChange: unit_load
    //    });

    $('#sql_filter_button').click(function() {
        //           console.log("clicked")
        filter_val = $('#sql_filter_val').val()
        $.ajax('/assessment/get_filter_unit_gdesg_list?filter=' + encodeURIComponent(filter_val), // request url
            {
                dataType: 'json', // type of response data
                timeout: 5000, // timeout milliseconds
                success: function(data, status, xhr) {
                    console.log(data)
                    $gdesg_table_area.setData(data.area_list);
                    $gdesg_table.setData(data.unit_list);
                    load_desg_summary_company(filter_val)
                },
                error: function(jqXhr, textStatus, errorMessage) { // error callback
                    console.log(textStatus, errorMessage)
                }
            });
    });
    function load_desg_summary_company(filter_val) {
        $.ajax('/assessment/get_desg_summary_company?filter=' + encodeURIComponent(filter_val), // request url
            {
                dataType: 'json', // type of response data
                timeout: 5000, // timeout milliseconds
                success: function(data, status, xhr) {
                    console.log(data)
                    $desg_table_company.setData(data.desg_summary_company);
                },
                error: function(jqXhr, textStatus, errorMessage) { // error callback
                    console.log(textStatus, errorMessage)
                }
            });
    }
    function load_desg_summary_area(filter_val, a_order) {
        $.ajax('/assessment/get_desg_summary_area?filter=' + encodeURIComponent(filter_val)+'&a_order='+a_order, // request url
            {
                dataType: 'json', // type of response data
                timeout: 5000, // timeout milliseconds
                success: function(data, status, xhr) {
                    console.log(data)
                    $desg_table_area.setData(data.desg_summary_area);
                    ($("#area_header")[0]).textContent=(data.desg_summary_area[0].a_name)+" : Area Level"
                },
                error: function(jqXhr, textStatus, errorMessage) { // error callback
                    console.log(textStatus, errorMessage)
                }
            });
    }

    function create_desg_table() {
        return new Tabulator("#desg_table", {
            // height:320, // set height of table (optional)
            keybindings: {
                "redo": "ctrl + 82", //bind redo function to ctrl + r,
                "navUp": "ctrl + 38",
                "navDown": "ctrl + 40",
                "navLeft": "ctrl + 37",
                "navRight": "ctrl + 39"
            },
            layout: 'fitColumns', //fit columns to width of table (optional)
            tooltips: true,
            columnCalcs: "table",
            headerSort: false,
            keybindings: true,

            initialSort: [{
                column: "d_gcode",
                dir: "asc"
            }, ],
            columns: [ //Define Table Columns
                {
                    title: "Designation",
                    field: "d_name",
                    width: 200
                },
                //                {
                //                    title: "Grade",
                //                    field: "d_grade",
                //                    align: "left",
                //                },
                {
                    title: "Code",
                    field: "d_id",
                    align: "left",
                    formatter: function(cell, formatterParams, onRendered) {
                        return cell.getValue().slice(-7);
                    }
                },
                {
                    title: "Grade",
                    field: "d_grade",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue();
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        if (d_cadre === 'XCD') {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return value;
                        }
                    }
                },
                {
                    title: "rank",
                    field: "d_gcode",
                    visible: false,
                    sorter: "number"
                },
                {
                    title: "Prev San",
                    field: "prev_san",
                    //                    editor: "number",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                    //                    formatter:function(cell, formatterParams){
                    //                        var value = cell.getValue() ? cell.getValue() : '';
                    //                        //console.log(cell.getData())
                    //                        var d_cadre = cell.getData().d_cadre
                    //                        var tot = cell.getData().tot
                    //
                    //                        if(d_cadre==='XCD' && tot < value){
                    //                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                    //                        }else{
                    //                            return "<span style='color:green; font-weight:bold;'>" + value + "</span>";
                    //                        }
                    //                    }
                },
                {
                    title: "Ext",
                    field: "tot",
                    align: "right",
                    bottomCalc: "sum",
                    formatter: function(cell, formatterParams, onRendered) {
                        // console.log(cell)
                        var data = cell.getData()
                        //                        x=cell
                        var url = '<a class=" light_link_column" target="_blank"  href="/assessment/emp/list/?e_unit_roll__u_id=' + data.u_id.slice(-6) + '&e_desg__d_id=' + data.d_id.slice(-7) + '">' + cell.getValue() + '</a>'
                        //                        return cell.getValue().slice(-7);
                        return url
                    },
                },
                {
                    title: "Ret",
                    field: "retr0",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0"
                },
                {
                    title: "Req",
                    field: "req",
                    editor: "number",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue() ? cell.getValue() : '';
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        var tot = cell.getData().tot
                        if (d_cadre === 'XCD' && tot < value) {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return "<span style='color:orange; font-weight:bold;'>" + value + "</span>";
                        }
                    }
                },
                {
                    title: "San",
                    field: "san",
                    editor: "number",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue() ? cell.getValue() : '';
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        var tot = cell.getData().tot

                        if (d_cadre === 'XCD' && tot < value) {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return "<span style='color:green; font-weight:bold;'>" + value + "</span>";
                        }
                    }
                },
                {
                    title: "Remark",
                    field: "comment",
                    editor: "input",
                    align: "left"
                },
            ],
            rowClick: function(e, row) { //trigger an alert message when the row is clicked
                // alert("Row " + row.getData().grade + " Clicked!!!!");
            },
            cellEdited: function(cell) {
                console.log(cell)
                var data = cell.getRow().getData()
                if (data.req === null || data.req === "")
                    data.req = 0
                if (data.san === null || data.req === "")
                    data.san = 0
//                if (data.san >= 0 && data.req >= 0)
                update_sanc_table(data)
            },
        });
    }

    function create_desg_table_area() {
        return new Tabulator("#desg_table_area", {
            layout: 'fitColumns', //fit columns to width of table (optional)
            tooltips: true,
            columnCalcs: "table",
            headerSort: false,
            keybindings: true,

            initialSort: [{
                column: "d_gcode",
                dir: "asc"
            }, ],
            columns: [ //Define Table Columns
                {
                    title: "Designation",
                    field: "d_name",
                    width: 200
                },
                {
                    title: "Code",
                    field: "d_id",
                    align: "left",
                    formatter: function(cell, formatterParams, onRendered) {
                        return cell.getValue().slice(-7);
                    }
                },
                {
                    title: "Grade",
                    field: "d_grade",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue();
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        if (d_cadre === 'XCD') {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return value;
                        }
                    }
                },
                {
                    title: "rank",
                    field: "d_gcode",
                    visible: false,
                    sorter: "number"
                },
                {
                    title: "Prev San",
                    field: "prev_san",
                    //                    editor: "number",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                },
                {
                    title: "Ext",
                    field: "tot",
                    align: "right",
                    bottomCalc: "sum",
                    formatter: function(cell, formatterParams, onRendered) {
                        // console.log(cell)
                        var data = cell.getData()
                        //                        x=cell
                        var url = '<a class=" light_link_column" target="_blank"  href="/assessment/emp/list/?e_unit_roll__u_id=' + data.u_id.slice(-6) + '&e_desg__d_id=' + data.d_id.slice(-7) + '">' + cell.getValue() + '</a>'
                        //                        return cell.getValue().slice(-7);
                        return url
                    },
                },
                {
                    title: "Ret",
                    field: "retr0",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0"
                },
                {
                    title: "Req",
                    field: "req",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue() ? cell.getValue() : '';
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        var tot = cell.getData().tot
                        if (d_cadre === 'XCD' && tot < value) {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return "<span style='color:orange; font-weight:bold;'>" + value + "</span>";
                        }
                    }
                },
                {
                    title: "San",
                    field: "san",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue() ? cell.getValue() : '';
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        var tot = cell.getData().tot

                        if (d_cadre === 'XCD' && tot < value) {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return "<span style='color:green; font-weight:bold;'>" + value + "</span>";
                        }
                    }
                },
                {
                    title: "Remark",
                    field: "comment",
                    editor: "input",
                    align: "left"
                },
            ],
        });
    }

    function create_desg_table_companytt() {
        return new Tabulator("#desg_table_company", {
            layout: 'fitColumns', //fit columns to width of table (optional)
            tooltips: true,
            columnCalcs: "table",
            headerSort: false,
            keybindings: true,

            initialSort: [{
                column: "d_gcode",
                dir: "asc"
            }, ],
            columns: [ //Define Table Columns
                {
                    title: "Designation",
                    field: "d_name",
                    width: 200
                },
                {
                    title: "Code",
                    field: "d_id",
                    align: "left",
                    formatter: function(cell, formatterParams, onRendered) {
                        return cell.getValue().slice(-7);
                    }
                },
                {
                    title: "Grade",
                    field: "d_grade",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue();
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        if (d_cadre === 'XCD') {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return value;
                        }
                    }
                },
                {
                    title: "rank",
                    field: "d_gcode",
                    visible: false,
                    sorter: "number"
                },
                {
                    title: "Prev San",
                    field: "prev_san",
                    //                    editor: "number",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                },
                {
                    title: "Ext",
                    field: "tot",
                    align: "right",
                    bottomCalc: "sum",
                    formatter: function(cell, formatterParams, onRendered) {
                        // console.log(cell)
                        var data = cell.getData()
                        //                        x=cell
                        var url = '<a class=" light_link_column" target="_blank"  href="/assessment/emp/list/?e_unit_roll__u_id=' + data.u_id.slice(-6) + '&e_desg__d_id=' + data.d_id.slice(-7) + '">' + cell.getValue() + '</a>'
                        //                        return cell.getValue().slice(-7);
                        return url
                    },
                },
                {
                    title: "Ret",
                    field: "retr0",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0"
                },
                {
                    title: "Req",
                    field: "req",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue() ? cell.getValue() : '';
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        var tot = cell.getData().tot
                        if (d_cadre === 'XCD' && tot < value) {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return "<span style='color:orange; font-weight:bold;'>" + value + "</span>";
                        }
                    }
                },
                {
                    title: "San",
                    field: "san",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0",
                    formatter: function(cell, formatterParams) {
                        var value = cell.getValue() ? cell.getValue() : '';
                        //console.log(cell.getData())
                        var d_cadre = cell.getData().d_cadre
                        var tot = cell.getData().tot

                        if (d_cadre === 'XCD' && tot < value) {
                            return "<span style='color:red; font-weight:bold;'>" + value + "</span>";
                        } else {
                            return "<span style='color:green; font-weight:bold;'>" + value + "</span>";
                        }
                    }
                },
                {
                    title: "Remark",
                    field: "comment",
                    editor: "input",
                    align: "left"
                },
            ],
        });
    }


    function update_sanc_table(data) {
        console.log(data)
        $.ajax({
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            url: "/assessment/set_req_unit_desg/",
            method: "POST", //First change type to method here
            data: data,
            success: function(response) {
                console.log("update row : sanction table success")
                var footer_result = ($desg_table.getCalcResults()).bottom;
                // console.log(footer_result)
                //                        $current_row_table1.update({freq:footer_result.req, fsan:footer_result.san})
                $current_row_table2.update({
                    freq: footer_result.req,
                    fsan: footer_result.san
                })
                var footer_result = ($gdesg_table.getCalcResults()).bottom;
                //                        var res = {freq:0.req, fsan:footer_result.san}
                //                      footer_result.keys(obj).forEach( function(key) { })
                console.log({
                    freq: footer_result.freq,
                    fsan: footer_result.fsan
                })

                $current_row_table1.update({
                    freq: footer_result.freq,
                    fsan: footer_result.fsan
                })

                var filter_val = $('#sql_filter_val').val()
                var data = $current_row_table2.getData()

                load_desg_summary_company(filter_val)
                load_desg_summary_area(filter_val, data.a_order)

                console.log(data)
                get_stat(data)
            },
            error: function() {
                //alert("error");
            }
        });
    }
    //load sample data into the table
    // $("#desg_table").tabulator("setData", "setData","http://www.getmydata.com/now");
    //$("#desg_table").tabulator("setData", desg_table_data);
    function create_sect_table() {
        return new Tabulator("#sect_table", {
            // height:320, // set height of table (optional)
            layout: 'fitColumns', //fit columns to width of table (optional)
            tooltips: true,
            columnCalcs: "table",
            headerSort: false,
            initialSort: [{
                column: "s_rank",
                dir: "asc"
            }, ],
            columns: [ //Define Table Columns
                {
                    title: "Section",
                    field: "s_name",
                    width: 200
                },
                {
                    title: "unit",
                    field: "unit",
                    visible: false
                },
                {
                    title: "d5",
                    field: "d5",
                    visible: false
                },
                {
                    title: "Location",
                    field: "s_location",
                    align: "left",
                },
                {
                    title: "Code",
                    field: "sect",
                    align: "left",
                    formatter: function(cell, formatterParams, onRendered) {
                        return cell.getValue().slice(-7);
                    },
                },

                {
                    title: "s_rank",
                    field: "s_rank",
                    visible: false,
                    sorter: "number"
                },
                //                {
                //                    title: "Prev San",
                //                    field: "prev_san",
                //                    editor: "number",
                //                    align: "right",
                //                    bottomCalc: "sum",
                //                    validator:"min:0"
                //                },
                {
                    title: "Ext",
                    field: "tot",
                    align: "right",
                    bottomCalc: "sum",
                    //                    formatter:function(cell, formatterParams, onRendered){
                    //                        console.log(cell)
                    //                        data = cell.getData()
                    //                        x=cell
                    //                        var url = '<a class="link_col_summ" target="_blank"  href="/assessment/emp/list/?e_unit_roll__u_code='+data.u_id.slice(-6)+'&e_desg__d_code='+data.d_id.slice(-7)+'">'+cell.getValue()+'</a>'
                    ////                        return cell.getValue().slice(-7);
                    //                        return  url
                    //                    },
                },
                {
                    title: "Ret",
                    field: "retr0",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0"
                },
                {
                    title: "Req",
                    field: "req",
                    editor: "number",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0"
                },
                {
                    title: "San",
                    field: "san",
                    editor: "number",
                    align: "right",
                    bottomCalc: "sum",
                    validator: "min:0"
                },
                {
                    title: "Remark",
                    field: "sns_comment",
                    editor: "input",
                    align: "left",
                },
            ],
            rowClick: function(e, row) { //trigger an alert message when the row is clicked
                // alert("Row " + row.getData().grade + " Clicked!!!!");
            },
            cellEdited: function(cell) {
                console.log(cell)
                var data = cell.getRow().getData()
                if (data.req === null)
                    data.req = 0
                if (data.san === null)
                    data.san = 0
                $.ajax({
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken")
                    },
                    url: "/assessment/set_req_unit_sect/",
                    method: "POST", //First change type to method here
                    data: data,
                    success: function(response) {
                        console.log("success")
                    },
                    error: function() {
                        alert("error");
                    }
                });
            },
        });
    }


    get_static_json_results()
    res_tables = create_gdesg_table()
    $gdesg_table_area = res_tables[0]
    $gdesg_table = res_tables[1]
    $desg_table = create_desg_table()
    $desg_table_area = create_desg_table_area()
    $desg_table_company = create_desg_table_companytt()

//    $sect_table = create_sect_table()




    $("#allot_buttton").click(function() {

        var val = +($('#sanc_dist').val())
        var promote = +($('#promote_value').val())

        var data = $desg_table.getData()
        col_cells = ($desg_table.getColumn("san")).getCells()

        if (val > 0)
            data.forEach(calc)

        var prev_promo = 0

        function calc(item, index, arr) {
            var curr_ext = item.tot ? item.tot : 0
            var resultant_ext = (prev_promo > 0 && curr_ext >= prev_promo) ? (curr_ext - prev_promo) : curr_ext
            var curr_sanc = item.san ? item.san : 0
            var last_row = index < arr.length - 1 ? false : true

            var next_ext = (!last_row) ? arr[index + 1].tot : 0
            var curr_cadre = item.d_cadre
            var next_cadre = (!last_row) ? arr[index + 1].d_cadre : null
            var promotion_scope = (curr_cadre === "XCD") ? 0 : Math.round(next_ext * promote)


            if (last_row) {
                (col_cells[index]).setValue(val)
                console.log("index:" + index + " => ", curr_ext, curr_sanc, val, +(val - val), promotion_scope, next_ext)
                val = val - val
            } else {
                var cell_value = 0
                if ((resultant_ext + promotion_scope) <= val) {
                    cell_value = resultant_ext + promotion_scope
                    prev_promo = promotion_scope
                } else {
                    cell_value = val
                }
                (col_cells[index]).setValue(cell_value)
                console.log("index:" + index + " => ", curr_ext, curr_sanc, resultant_ext + promotion_scope, (val - resultant_ext), promotion_scope, next_ext)
                val = (val - cell_value)

            }
        }

    });

    //trigger download of data.pdf file
    $("#download-pdf").click(function() {
        var data = {
            report: 'funit_dscd_er',
            param: {
                u_id: $current_sel_unit
            },
            file_format: 'pdf'
        };

        fetch('/assessment/report_download/', {
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            method: 'POST',
            body: JSON.stringify(data),
        }).then(function(resp) {
            return resp.blob();
        }).then(function(blob) {
            return download(blob, $current_sel_unit + ".pdf");
        });

        //    $gdesg_table.download("pdf", "data.pdf", {
        //        orientation:"portrait", //set page orientation to portrait
        //        title:"Example Report", //add title to report
        //    });
        //html_to_pdf('#gdesg_table')
    });


    // look for url query string, if u_id is present then load the data
    //var filter_val = getParameterByName("u_id");
    //console.log(filter_val)
    //if (filter_val){
    //$('#combo_div').hide()
    //// $('#unit_select').dropdown('set selected', filter_val)
    //unit_load(filter_val)
    //}


});