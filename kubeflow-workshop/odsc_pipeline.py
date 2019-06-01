import kfp.dsl as dsl
import kubernetes.client.models as k8s
import argparse



@dsl.pipeline(name="ODSC test pipeline", description="Some desc")
def odsc_pipeline(
      model_name="",
      mount_path="/storage"
):
    download=dsl.ContainerOp(
        name="download",
        image="",
        arguments=[
            "--mount_path", mount_path
        ],
        file_outputs={
            "data_path":"/data_path.txt"
        }
    )

if __name__ == "__main__":
    import kfp.compiler as compiler
    import subprocess, sys

    # Parse namespace
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file', help='New pipeline file', default="pipeline.tar.gz")
    parser.add_argument(
        '-n', '--namespace', help="Namespace, where kubeflow and serving are running", required=True)
    args = parser.parse_args()
    arguments = args.__dict__

    namespace, file = arguments["namespace"], arguments["file"]
    compiler.Compiler().compile(pipeline_definition, file)

    untar = f"tar -xvf {file}"
    replace_minio = f"sed -i '' s/minio-service.kubeflow/minio-service.{namespace}/g pipeline.yaml"
    replace_pipeline_runner = f"sed -i '' s/pipeline-runner/{namespace}-pipeline-runner/g pipeline.yaml"

    process = subprocess.run(untar.split())
    process = subprocess.run(replace_minio.split())
    process = subprocess.run(replace_pipeline_runner.split())