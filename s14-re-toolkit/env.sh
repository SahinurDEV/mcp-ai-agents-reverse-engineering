# env.sh: source me. Where Ghidra, the JDK and the GhidraMCP 2.0 jar live on this box.
export GHIDRA_INSTALL_DIR=${GHIDRA_INSTALL_DIR:-/workspace/tools/ghidra/ghidra_12.1.4_PUBLIC}
export JAVA_HOME=${JAVA_HOME:-/workspace/tools/jdk/current}
export GHIDRAMCP_JAR=${GHIDRAMCP_JAR:-/workspace/tools/ghidramcp/ext/GhidraMCP/lib/GhidraMCP.jar}
