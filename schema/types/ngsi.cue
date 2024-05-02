package types

import (
	"strings"
)

// Schema básico de un atributo de modelo
#ModelAttribute: {
	description: string
	ngsiType:    string
	dbType:      string
	extra:       string | *"-"
	unit:        string | *"-"
	example:     _
	range:       string | *"-"
	// Permito especificar el rango como un array
	// en lugar de un simple string, usando #range
	#range: [...string]
	if len(#range) > 0 {
		example: #range[0]
		range:   strings.Join(#range, ", ")
	}
	flows: [...string]
}

#DateTime: #ModelAttribute & {
	ngsiType: "DateTime"
	dbType:   "timestamp with time zone NOT NULL"
	example:  string | *"2018-12-10T20:40:23"
}

#DateTimeNull: #ModelAttribute & {
	ngsiType: "DateTime"
	dbType:   "timestamp with time zone"
	example:  string | *"2018-12-10T20:40:23"
}

#Text: #ModelAttribute & {
	ngsiType: "TextUnrestricted"
	dbType:   "text"
	example:  string | *"example text"
}

#TextUnrestricted: #ModelAttribute & {
	ngsiType: "TextUnrestricted"
	dbType:   "text"
	example:  string | *"example text"
}

#Bool: #ModelAttribute & {
	ngsiType: "Bool"
	dbType:   "bool"
	example:  bool | *false
}

#Integer: #ModelAttribute & {
	ngsiType: "Number"
	dbType:   "int"
	example:  number | *5
}

#Double: #ModelAttribute & {
	ngsiType: "Number"
	dbType:   "double precision"
	example:  number | *5.0
}

#Json: #ModelAttribute & {
	ngsiType: "TextUnrestricted"
	dbType:   "json"
	example:  _
}

#Array: #ModelAttribute & {
	ngsiType: "Json"
	dbType:   "json"
	example: [...string]
}

#Geometry: Point: #ModelAttribute & {
	ngsiType: "geo:json"
	dbType:   "geometry(Point)"
	example: {
		type: "geo:json"
		value: {
			type: "Point"
			coordinates: [3.5, 24.6]
		}
	}
}

#Geometry: Line: #ModelAttribute & {
	ngsiType: "geo:json"
	dbType:   "geometry(Line)"
	example: {
		type: "geo:json"
		value: {
			type: "Line"
			coordinates: [[3.5, 24.6], [33, 44]]
		}
	}
}

#Geometry: MultiLine: #ModelAttribute & {
	ngsiType: "geo:json"
	dbType:   "geometry(MultiLine)"
	example: {
		type: "geo:json"
		value: {
			type: "Line"
			coordinates: [[[3.5, 24.6], [33, 44]]]
		}
	}
}
