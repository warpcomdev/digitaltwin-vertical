package cmd

import (
	"text/template"
	"strings"
	"tool/file"
	"github.com/telefonicasc/digitaltwin-vertical/schema/models"
)

#filename: string @tag(filename)
#model:    string @tag(model)
#section:  string @tag(section)

command: export: do: file.Create & {
	filename: #filename
	contents: strings.Join([for label, sect in models[#model].#export[#section] {
		template.Execute(sect.template, sect.input)
	}], "\n\n")
}
