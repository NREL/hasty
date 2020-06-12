/**
 * Retrieve and parse out a project haystack grid (in JSON form)
 * as nodes and edges.
 */



var data;

var is_ref = function(val) {
	return (typeof(val) === 'string') && val.startsWith('r:');
};

var parse_ref = function(val) {
	//return val.substring(2).split(' ',1)[0];		
	return "id: " + val
};

var is_marker = function(val) {
	return (typeof(val) === 'string') && val.startsWith('m:');
};


var on_receive_data = function(hs_data) {
	var nodes = [];
	var edges = [];

	hs_data.rows.forEach(function (row) {
		var id = parse_ref(row.id);
		var site = is_marker(row.site);
		var equip = is_marker(row.equip);
		var point = is_marker(row.point);
		var weather = is_marker(row.weather);
		var space = is_marker(row.space);

		var node = {
			id: id,
			size: 100,
			label: id,
			shape: 'box',
			font: {
				face: 'arial',
				align: 'left',
			},
			site: false,
			equip: false,
			point: false,
			weather: false,
			space: false
		};
		nodes.push(node);
		//console.log('New node: ' + id);

		/* Iterate over the other tags */
		Object.keys(row).forEach(function (tag) {

			if (tag == 'id')
				return;
			
			var val = row[tag];

			if (val === 'm:') {
				/* Marker tag */
				node.label += '\n' + tag;
			}

			if	((typeof(val) === 'string') && val.startsWith('s:')) {
				/*String Tag*/
				node.label += '\n' + tag +': \''+val.replace('s:','')+'\'';
			}

			if ((typeof(val) === 'string') && val.startsWith('r:')) {
				node.label += '\n' + tag +': \''+val.replace('r:','')+'\'';
			}

			if (point) {
				node.group='point';
				node.mass=1
			}
			if (equip) {
				node.group='equip'
				node.mass=4
			}
			if (site) {
				node.group='site';
				node.mass=20
			}
			if (weather)
				node.group='weather'
			if (space)
				node.group='space'

			if (!is_ref(val))
				return;
			
			var dest = parse_ref(val);
			//console.log('New edge: tag ' + tag + ' id ' + id + ' to ' + dest);
			edge = {
				from: id,
				to: dest,
				label: tag,
				title: tag,
				arrows: 'to',
				physics: true,
				smooth: {
					type: 'continuous',
					roundness: 0
				}
			} 
			edges.push(edge);

			if (tag === 'siteRef' && point) {
				edge.value = 4;
				edge.length = 8;
				//console.log('value : ' + edge.value);
			}
			if (tag === 'siteRef' && equip) {
				edge.value = 8;
				edge.length = 0.1;
				//console.log('value : ' + edge.value);
			}
			if (tag === 'equipRef' && equip) {
				edge.value = 8;
				edge.length = 8;
				//console.log('value : ' + edge.value);
			}
			if (tag === 'equipRef' && point) {
				edge.value = 8;
				edge.length = 0.1;
				//console.log('value : ' + edge.value);
			}
			
		});
	});
	
    
    var data = {
        nodes: nodes,
        edges: edges
    };

	return data;

};



function load_entities(url) {
    return new Promise(function (resolve, reject) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.onload = resolve;

        xhr.onerror = reject;
        xhr.send();
    });
}




