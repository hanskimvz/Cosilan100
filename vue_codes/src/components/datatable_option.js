// import { useI18n } from 'vue-i18n';

export function getDataTableOptions(t) {
    return {
      select: { style: 'single' },
      pagingType: 'simple_numbers',
      autoFill: true,
      language: {
        "decimal": "",
        "emptyTable": t('data_table_empty_table'),
        "info": t('data_table_info'),
        "infoEmpty": t('data_table_info_empty'),
        "infoFiltered": t('data_table_filtered_from_max'),
        "infoPostFix": "",
        "thousands": ",",
        "lengthMenu": t('data_table_length_menu'),
        "loadingRecords": t('data_table_loading'),
        "processing": "",
        "search": t('data_table_search') + ": ",
        "zeroRecords": t('data_table_no_matching_record'),
        "paginate": {
          "first": t('data_table_first'),
          "last": t('data_table_last'),
          "next": t('data_table_next'),
          "previous": t('data_table_previous')
        },
        "aria": {
          "orderable": "Order by this column",
          "orderableReverse": "Reverse order this column"
        },
        "select": {
          rows: t('data_table_select')
        }
      },
      layout: {
        topStart: {
          buttons: ['copy', 'csv', 'excel']
        },
        topEnd: ['search'],
        bottomStart: ['info'],
        bottomEnd: [
          { pageLength: {} },
          {
            paging: {
              type: 'full_numbers',
              buttons: 5,
              className: "btn btn-sm"
            }
          }
        ]
      }
    };
  }