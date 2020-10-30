

var get_options = function() {

  var options = {
    autoResize: true,
    manipulation: true,
      height: '100%',
      width: '100%',
      manipulation: {
        enabled: false
    },
      layout: {
        improvedLayout: true
      },


    nodes: {
        font: {
          color: '#343434',
          size: 28, // px
          face: 'arial',
          background: 'none',
          strokeWidth: 0, // px
          strokeColor: '#ffffff',
          align: 'top',
          multi: false,
          vadjust: 0
      },
      margin: {
        top: 10,
        left: 10,
        bottom: 10,
        right: 10
      },
      widthConstraint: { minimum: 250 },
      heightConstraint: { minimum: 200 }
      },

    edges:{
        color: {inherit: 'to'},
      scaling:{
            min: 1,
            max: 10,
            label: {
              enabled: true,
              min: 14,
              max: 30,
              maxVisible: 30,
              drawThreshold: 5
            },
        },
      },

      physics: {
        enabled: true,
        solver: 'hierarchicalRepulsion',
        hierarchicalRepulsion: {
          centralGravity: 10,
          springLength: 1,
          springConstant: 100,
          nodeDistance: 2500,
          damping: 20
          },
        minVelocity: 200,
        maxVelocity: 1600,
        timestep: 0.01,
        stabilization: {
          enabled: true,
          iterations: 2000,
          updateInterval:50,
          fit: true
        },



      },
      groups: {
        site: {color:{border:'#6f79a8', background:'#9fa8da'}, borderWidth:1},
        equip: {color:{border:'#4ba3c7', background:'#81d4fa'}, borderWidth:1},
        point: {color:{border:'#bcbcbc', background:'#eeeeee'}, borderWidth:1},
        weather: {color:{border:'#4dd0e1', background:'#4dd0e1'}, borderWidth:1},
        space: {color:{background:'grey'}, borderWidth:0}
      }
  };

  return options
};
