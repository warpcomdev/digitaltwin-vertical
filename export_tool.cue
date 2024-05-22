package cmd

import (
	"text/template"
	"strings"
	"list"
	"tool/file"
	"encoding/json"
	"github.com/telefonicasc/digitaltwin-vertical/schema/models"
)

#filename: string @tag(filename) // nombre del fichero de salida

#model: string | *"" @tag(model) // modelo a volcar, dejar vacío para "todos los modelos"

#section: string @tag(section) // nombre de la sección de exportación a volcar

#json: bool | *false @tag(json,type=bool) // volcar el resultado como json

command: export: {

	sections: _

	// If a model name is specified, get only templates for that model
	if #model != "" {
		sections: [for _, sect in models[#model].#export[#section] {sect}]
	}

	// Otherwise, all models are included
	if #model == "" {
		sections: list.FlattenN([for _, model in models if model.#export != _|_ {
			[for _, sect in model.#export[#section] {sect}]
		}], -1)
	}

	// Create a file with all sections concatenated and
	// separaded by the #separator
	if !#json {
		do: file.Create & {
			filename: #filename
			contents: strings.Join([for _, sect in sections {
				template.Execute(sect.template, sect.input)
			}], "\n")
		}
	}

	// dump the section to json instead
	if #json {
		do: file.Create & {
			filename: #filename
			contents: json.Indent(json.Marshal([for _, sect in sections {
				sect.input
			}]), "", "  ")
		}
	}
}
