/**
 * UCA javascript implementation based on the pyuca code by James Tauber http://jtauber.com/
 * See http://www.unicode.org/reports/tr10 for UCA specification
 * @author Santhosh Thottingal 
 * @date 17 May 2012s
 * @copyright GPLv2+
 */

/*
NOTE: This code require a trie in json format generated from the Unicode DUCET. See pyuca.py along with this code

A sample trie will look like this:
trie = [null, {"3390": [[[".", ["21D5", "0020", "0002", "0D3E"]]], {}], "3398": [null, {"3390": [[[".", ["21E1", "0020", "0002", "0D4A"]]], {}]}], "3399": [null, {"3390": [[[".", ["21E2", "0020", "0002", "0D4B"]]], {}]}], "3403": [[[".", ["21E2", "0020", "0002", "0D4B"]]], {}]}];

*/

function find_prefix( trie, key ){
	var curr_node = trie;
	var remainder = key;
	for ( var i = 0; i < key.length; i++ ) {
		part = key[i];
		if( !curr_node[1].hasOwnProperty( part ) ){
			break;
		}
		curr_node = curr_node[1][part];
		remainder = remainder.slice( 1 );
	}
	return [curr_node[0], remainder];
}

function sort_key( string ){
	var collation_elements = [];
	var lookup_key = [];
	for( var i=0; i< string.length; i++ ){
		lookup_key.push( string.charCodeAt(i) );
	}
	prefix = find_prefix( trie, lookup_key );
	value = prefix[0];
	lookup_key = prefix[1];
	if( !value ) {
		console.log( "error" );
		return 0;
	} else {
		collation_elements= value;
	}
	var sort_key = [];
	for( level = 0; level<4; level++ ){
		if( level ){
			sort_key.push(0);
		}
		for( var i=0; i< collation_elements.length; i++ ){
			element = collation_elements[i];
			//sort_key.push(int(element[1][level], 16));
			sort_key.push(element[1][level]);
		}
	}
	return sort_key.join( ',' );
}

