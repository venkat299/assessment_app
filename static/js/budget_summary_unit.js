
//'u_id', 'u_name', 'u_type', 'u_code', 'a_name', 'a_order', 'acde',
function on_page_load(area_summary, unit_summary){
var summary_table_area =new Tabulator("#area_summary_table", {
            //height:400,
//            layout:"fitColumns",

            tooltips: true, //show tool tips on cells
            history: false, //allow undo and redo actions on the table
            movableColumns: false, //allow column order to be changed
            resizableRows: false, //allow row order to be changed
            headerSort: false,
//            groupBy: "a_name",
//            groupStartOpen:false,
//            groupClosedShowCalcs:true,
             columnCalcs:"both",
            placeholder:"No Data Available",
            data :area_summary,
//             footerElement:"<button>Custom Button</button>",
//            initialSort: [ //set the initial sort order of the data
//                {
//                    column: "a_order",
//                    dir: "asc"
//                },
//            ],
            //'u_id', 'u_name', 'u_type', 'u_code', 'a_name', 'a_order', 'acde',
            columns: [ //define the table columns
                {
                    title: "Area Name",
                    field: "a_name",
                    width: 200,
//                    headerFilter: "input"
                },
                {title:"Area code", field:"acde", visible:false },
                {
                    title: "Ext",
                    field: "ftot",
//                    bottomCalc: "sum",
                     width: 100,
                    bottomCalc:"sum",

                    align: "right",
//                    formatter:function(cell, formatterParams, onRendered){
//                       // console.log(cell)
//                        var data = cell.getData()
//                        x=cell
//                        var url = '<a class="light_link_column" target="_blank"  href="/assessment/emp/list/?e_unit_roll__u_code='+data.u_id.slice(-6)+'&e_desg__d_code='+data.d5.slice(-7)+'">'+cell.getValue()+'</a>'
//                        return cell.getValue().slice(-7);
//                        return url
//                    },
                },
//                {
//                    title: "Ret",
//                    field: "fret",
//                    align: "right",
////                    width: 50,
//                    bottomCalc: "sum",
//                },
                {
                    title: "Req",
                    field: "freq",
                    width: 100,
                    bottomCalc: "sum",
                    align: "right"
                },
                {
                    title: "San",
                    field: "fsan",
                    align: "right",
                    width: 100,
                     bottomCalc: "sum",
                }
            ],
            rowClick: function(e, row) {
                //e - the click event object
                //row - row component
                $current_row = row
                var data = row.getData()
//                console.log(data)
                summary_table_unit.clearFilter();
                summary_table_unit.setFilter("acde", "=", data.acde);
            },
        });


var summary_table_unit =new Tabulator("#unit_summary_table", {
            height:600,
//            layout:"fitColumns",
            tooltips: true, //show tool tips on cells
            history: false, //allow undo and redo actions on the table
            movableColumns: false, //allow column order to be changed
            resizableRows: false, //allow row order to be changed
            headerSort: false,
//            groupBy: "a_name",
//            groupStartOpen:false,
//            groupClosedShowCalcs:true,
//             columnCalcs:"both",
            placeholder:"No Data Available",
            data :unit_summary,
//             footerElement:"<button>Custom Button</button>",
//            initialSort: [ //set the initial sort order of the data
//                {
//                    column: "a_order",
//                    dir: "asc"
//                },
//            ],
            //'u_id', 'u_name', 'u_type', 'u_code', 'a_name', 'a_order', 'acde',
            columns: [ //define the table columns
                {
                    title: "Unit Name",
                    field: "u_name",
                    width: 200,
//                    headerFilter: "input"
                    formatter:function(cell, formatterParams, onRendered){
//                       console.log(cell)
                        var data = cell.getData()
//                        x=cell;
                        var url = '<a class="light_link_column" target="_blank"  href="/assessment/unit_req/?u_id='+data.u_id+'">'+cell.getValue()+'</a>'
//                        return cell.getValue().slice(-7);
                        return url
                    },
                },
                                {
                    title: "Area",
                    field: "acde",
//                    visible: false
                },
                                {
                    title: "Type",
                    field: "u_type",
                    width: 50,
//                    headerFilter: "input"
                },
                {
                    title: "Ext",
                    field: "ftot",
//                    bottomCalc: "sum",
                     width: 200,
//                    topCalc:"sum",

                    align: "right",
//                    formatter:function(cell, formatterParams, onRendered){
//                       // console.log(cell)
//                        var data = cell.getData()
//                        x=cell
//                        var url = '<a class="light_link_column" target="_blank"  href="/assessment/emp/list/?e_unit_roll__u_code='+data.u_id.slice(-6)+'&e_desg__d_code='+data.d5.slice(-7)+'">'+cell.getValue()+'</a>'
//                        return cell.getValue().slice(-7);
//                        return url
//                    },
                },
//                {
//                    title: "Ret",
//                    field: "fret",
//                    align: "right",
////                    width: 50,
//                    bottomCalc: "sum",
//                },
                {
                    title: "Req",
                    field: "freq",
                    width: 200,
//                    topCalc: "sum",
                    align: "right"
                },
                {
                    title: "San",
                    field: "fsan",
                    align: "right",
                    width: 200,
//                     topCalc: "sum",
                }
            ],
//            rowClick: function(e, row) {
//                //e - the click event object
//                //row - row component
//                $current_row = row
//                var data = row.getData()
//                console.log(data)
//                $.ajax('/assessment/get_req_unit_desg?u_id=' + data.u_id + '&d5=' + data.d5, // request url
//                    {
//                        dataType: 'json', // type of response data
//                        timeout: 500, // timeout milliseconds
//                        success: function($data, status, xhr) {
////                            console.log(data)
//                            $desg_table.setData($data);
////                            $("#desg_table").tabulator("setData", data);
//                        },
//                        error: function(jqXhr, textStatus, errorMessage) { // error callback
//                            //        $('p').append('Error: ' + errorMessage);
//                        }
//                    });
//                $.ajax('/assessment/get_req_unit_sect?u_id=' + data.u_id + '&d5=' + data.d5, // request url
//                    {
//                        dataType: 'json', // type of response data
//                        timeout: 500, // timeout milliseconds
//                        success: function($data, status, xhr) {
////                            console.log(data)
//                            $sect_table.setData($data);
//                        },
//                        error: function(jqXhr, textStatus, errorMessage) { // error callback
//                            //        $('p').append('Error: ' + errorMessage);
//                        }
//                    });
//            },
        });



}

