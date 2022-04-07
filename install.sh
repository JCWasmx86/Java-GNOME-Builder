#!/usr/bin/env bash
setupFile() {
	if [ -n "$G_VERSION" ]; then
		cat jdtls.plugin.in|sed s/XXXXX/$G_VERSION/g > jdtls.plugin
	else
		cat jdtls.plugin.in|sed s/XXXXX/43.0/g > jdtls.plugin
	fi
	if [ "$PATCHED" == "1" ]; then
		echo Using patched GNOME-Builder
		sed -i s/#123#//g jdtls.plugin
	else
		echo Using unpatched GNOME-Builder, codeactions won\'t work
		sed -i s/#123#.*//g jdtls.plugin
	fi
}
installToLocal() {
	cp jdtls.{py,plugin} ~/.local/share/gnome-builder/plugins
	if [ $PATCHED == "0" ]; then
		sed -i s/#123#.*//g ~/.local/share/gnome-builder/plugins/jdtls.py
		sed -i s/#124#//g ~/.local/share/gnome-builder/plugins/jdtls.py
	else
		sed -i s/#123#//g ~/.local/share/gnome-builder/plugins/jdtls.py
	fi
}
if [ "$1" == "--unpatched" ]; then
	export PATCHED=0
else
	export PATCHED=1
fi
rm -rf tmp ~/.local/share/jdtls
mkdir tmp
cd tmp
wget https://download.eclipse.org/jdtls/milestones/1.9.0/jdt-language-server-1.9.0-202203031534.tar.gz
tar xzvf jdt-language-server-1.9.0-202203031534.tar.gz
rm -rf ~/.local/share/jdtls
mkdir ~/.local/share/jdtls
cp -r plugins features ~/.local/share/jdtls
cp -r config_linux ~/.local/share/jdtls/config
{
	echo "#!/usr/bin/env bash"
	echo $(which java) -Declipse.application=org.eclipse.jdt.ls.core.id1 -Dosgi.bundles.defaultStartLevel=4 -Declipse.product=org.eclipse.jdt.ls.core.product -Dlog.level=ALL -Xmx"\$(printf '%.0fG' \$(free -h|sed 's/  */ /g'|cut -d ' ' -f2|head -n 2|tail -n 1|sed s/Gi/\\\\/4/|bc -l))" --add-modules=ALL-SYSTEM --add-opens java.base/java.util=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED -jar \~/.local/share/jdtls/plugins/org.eclipse.equinox.launcher_1.6.400.v20210924-0641.jar -configuration \~/.local/share/jdtls/config -data "\$1" 2>/tmp/jdtls_err.log | tee /tmp/jdtls_out.log
} > ~/.local/bin/jdtls
cd ..
# The sed lines are from https://github.com/Prince781/vala-language-server/blob/master/plugins/gnome-builder/get_builder_abi.sh
if ! command -v gnome-builder &> /dev/null; then
	echo GNOME Builder not found as a normal installed package
	if [ $(flatpak list|grep org.gnome.Builder|wc -l) == "1" ]; then
		echo Found GNOME Builder as a flatpak
		export G_VERSION=$(flatpak run org.gnome.Builder --version | sed -nr '/GNOME Builder/ { s/GNOME Builder ([[:digit:]]+\.[[:digit:]]+).*$/\1/ p }')
		setupFile
		installToLocal
	else
		echo GNOME-Builder is not installed
		exit 1
	fi
else
	echo GNOME-Builder found as a normal installed package
	export G_VERSION=$(gnome-builder --version | sed -nr '/GNOME Builder/ { s/GNOME Builder ([[:digit:]]+\.[[:digit:]]+).*$/\1/ p }')
	setupFile
	installToLocal
fi
