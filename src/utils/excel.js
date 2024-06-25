
export function transformDataForExcel(jsonData) {
    const columns = [
      'title', 'pub_time', 'area',  'source', 'first_url',
      'cp_source', 'is_cp', 'cp_title', 'cp_org', 'cp_org_url',
      'key_word','is_new_org', 'keyword_owner', 'is_publish'
    ];
    
    return jsonData.data.map(item => (
      columns.map(column => (item.fields[column] || ''))
    ));
  }
