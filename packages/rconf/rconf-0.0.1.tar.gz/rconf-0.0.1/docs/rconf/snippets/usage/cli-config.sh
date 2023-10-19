folder=`dirname -- "$0"`

rconf -c ${folder}/config.toml dump -p config.dump - << 'EOF'
[config]
$ref = ppr://rconf/scripts/rconf.toml

EOF
