function displaySelect(){
    if (document.getElementById("categorizetypelevel").checked) {
        document.getElementById("levelbasedtype").style.display = '';
        document.getElementById("trendbasedtype").style.display = 'none';
        document.getElementById("trendbasedtypetextdiv").style.display = 'none';
      }
    if (document.getElementById('categorizetypetrend').checked) {
        document.getElementById("trendbasedtype").style.display = '';
        document.getElementById("trendbasedtypetextdiv").style.display = '';
        document.getElementById("levelbasedtype").style.display = 'none';
      }
      if (document.getElementById("custombin").checked) {
        document.getElementById("customsizediv").style.display = '';
      }
      else {
          document.getElementById("customsizediv").style.display = 'none';
      }
      // if (document.getElementById("multitime").checked) {
      //   document.getElementById("multiseriestypetextdiv").style.display = '';
      //   document.getElementById("custombin").disabled = true;
      // }
      // if(document.getElementById("singletime").checked){
      //   document.getElementById("multiseriestypetextdiv").style.display = 'none';
      //   document.getElementById("custombin").disabled = false;
      // }
      
}


