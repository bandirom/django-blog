#!/bin/bash


help() {
    echo ""
    echo "Usage: build.sh [--linter <string>] [--build <string>] [--test]"
    echo "-l, --linter         <string>    Linter to run (black, isort, flake8)"
    echo "-b, --build          <string>    Build type (frontend, backend)"
    echo "-h, --help           <string>    Print this help message"
    echo "-t, --test           <string>    Test type (backend)"
    echo
}

install_dependencies() {
    pip install -r requirements.txt
}

run_black() {
    echo "Running Black..."
    black --check --diff .
}

run_isort() {
    echo "Running isort..."
    isort --check --diff .
}

run_flake8() {
    echo "Running Flake8..."
    flake8 .
}


validate_image_args() {
    IMAGE_NAME=${IMAGE_NAME:-$CI_REGISTRY_IMAGE} # "registry.gitlab.com/mds7060534/naivebayes_app/backend"
    APP_VERSION=${APP_VERSION:-$CI_COMMIT_REF_SLUG}
    PROJECT_PATH=${build_path}

    if [ -z "${IMAGE_NAME}" ]; then
      echo "Docker image not specified. Please provide -i | --image-name"
      echo "Supported env vars: DOCKER_IMAGE | CI_REGISTRY_IMAGE"
      exit 1
    fi

    if [ -z "${APP_VERSION}" ]; then
      echo "Docker image not specified. Please provide -v | --version"
      echo "Supported env vars: APP_VERSION | CI_COMMIT_REF_SLUG"
      exit 1
    fi

    IMAGE=${IMAGE_NAME}/${PROJECT_PATH}:${APP_VERSION}

    echo "Image Name: ${IMAGE_NAME}"
    echo "App Version: ${APP_VERSION}"
    echo "Project Path: ${PROJECT_PATH}"
    echo "Image: ${IMAGE}"
}

run_build() {

    validate_image_args

    CI_PROJECT_DIR=$(pwd)
    DOCKERFILE_PATH="./Dockerfile"
    CONTEXT="${CI_PROJECT_DIR}/${PROJECT_PATH}"

    /kaniko/executor --context "${CONTEXT}" --dockerfile "${DOCKERFILE_PATH}" --destination "${IMAGE_NAME}"
}

run_test() {
  validate_image_args

  docker pull $IMAGE
  docker run --entrypoint="" --rm --name $PROJECT_PATH $IMAGE python -m coverage run -m unittest discover -s tests -p *_test.py
}

# Main function to execute linting tasks based on the specified linter

if [ $# -eq 0 ]; then
    echo "No arguments provided. Usage: ./build.sh --help"
    exit 1
fi


main() {
    while [[ $# -gt 0 ]]; do
        key="$1"
        case "$key" in
            -l|--linter)
                linter="$2"
                shift; shift;
            ;;
            -b|--build)
                build="$2"
                build_path="$2"
                shift; shift;
            ;;
            -t|--test)
                test="$2"
                build_path="$2"
                shift; shift;
            ;;
            -h|--help)
                help
                exit 0;
            ;;
            -i|--image-name)
                IMAGE_NAME="$2"
                shift; shift;
                ;;
            -v|--version)
                APP_VERSION="$2"
                shift; shift;
            ;;
            *)
                echo "Invalid argument: $key"
                help
                exit 1
            ;;
        esac
    done
}


main "$@"


if [ "$linter" ]; then
    case "$linter" in
        black)
            run_black "$@"
        ;;
        isort)
            run_isort "$@"
        ;;
        flake8)
            run_flake8 "$@"
        ;;
        *)
            echo "Invalid linter: $linter"
            exit 1
        ;;
    esac
fi

if [ "$build" ]; then
    case "$build" in
        frontend)
            run_build "$@"
            ;;
        backend)
            run_build "$@"
            ;;
        *)
            echo "Invalid build: $build"
            exit 1
            ;;
    esac
fi

if [ "$test" ]; then
    case "$test" in
        backend)
            run_test "$@"
            ;;
        *)
            echo "Invalid test: $test"
            exit 1
            ;;
    esac
fi
