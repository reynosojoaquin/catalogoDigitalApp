export default {
    data () {
      return {
     
      }
    },
    methods:
    {
        getMaxID: function(data,property){
            let max=0;
            for(let i =0; i<data.length;i++){
              if(max < data[i][property]){
                max = data[i][property]
              }
            }
            return max
          },
          filtrarJson(json,  columna, valor) {
            let filteredJson = json.filter(e => e[columna] === valor);
            let newJson =  JSON.parse(JSON.stringify(filteredJson));  
           return newJson;
         }
    }
  }