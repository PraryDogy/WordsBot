function myFunction() {
    var ss=SpreadsheetApp.getActiveSpreadsheet();
    var s=ss.getActiveSheet();
    var 
    c=s.getActiveCell();
  
    var fldr=DriveApp.getFolderById("1IFJT-V6F7zMtbW4oaC5jGw9IAHNerJMI");
    var files=fldr.getFiles();
  
    var urls=[],f,str;
    var names_urls=[], f, str;
  
    while (files.hasNext()) {
      f=files.next();
  
      str=f.getUrl();
      urls.push([str]);
  
      nnm = f.getName();
      names_urls.push([nnm]);
    }
    s.getRange(c.getRow(),c.getColumn(),urls.length).setValues(urls);
    s.getRange(c.getRow(), c.getColumn() + 1, names_urls.length).setValues(names_urls);
  }
