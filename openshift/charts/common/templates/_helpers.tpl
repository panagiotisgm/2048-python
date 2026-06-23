# ── openshift/charts/common/templates/_helpers.tpl ────────────────────────────
# Shared named templates — defined once here, used across all deploy charts.
# Import by declaring common as a dependency in deploy/Chart.yaml.
# ──────────────────────────────────────────────────────────────────────────────

{{/*
Standard labels — stamped on every resource automatically.
Avoids copy-pasting the same label block into every manifest.
*/}}
{{- define "common.labels" -}}
app.kubernetes.io/name: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
team: platform
{{- end }}

{{/*
Selector labels — kept minimal so selectors don't break on upgrades.
Only stable identity fields go here.
*/}}
{{- define "common.selectorLabels" -}}
app.kubernetes.io/name: {{ .Release.Name }}
{{- end }}

{{/*
Image reference helper — builds the full image string from values.
Usage: {{- include "common.image" . }}
*/}}
{{- define "common.image" -}}
{{ .Values.image.repository }}:{{ .Values.image.tag }}
{{- end }}
