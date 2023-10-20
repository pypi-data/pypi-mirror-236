import base64
import re
import time

from layernext.datalake.annotation import Annotation
from layernext.datalake.metadata import Metadata
from layernext.datalake.query import Query

from .ground_truth import GroundTruth
from .constants import BOX_ANNOTATION, POLYGON_ANNOTATION, LINE_ANNOTATION, AnnotationUploadType, MediaType, JobStatus, ObjectType
from .datalakeinterface import DatalakeInterface
from .file_upload import FileUpload
from .file_trash import FileTrash
from .label import Label
from .logger import get_debug_logger
from .model_run import ModelRun

datalake_logger = get_debug_logger('DatalakeClient')


class DatalakeClient:
    """
    Python SDK of Datalake
    """

    def __init__(self, encoded_key_secret: str, layernext_url: str) -> None:
        _datalake_url = f'{layernext_url}/datalake'
        # _datalake_url = f'{layernext_url}'
        self.datalake_interface = DatalakeInterface(encoded_key_secret, _datalake_url)

    def check_sdk_version_compatibility(self, sdk_version: str):
        """
        check sdk version compatibility
        """

        if re.compile(r'^(\d+\.)+\d+$').match(sdk_version) is None:
            raise Exception('sdk_version is invalid format')

        if sdk_version is None or sdk_version == '' :
            raise Exception('sdk_version is None')
        
        res = self.datalake_interface.check_sdk_version_compatibility(sdk_version)

        if res["isCompatible"] == False:
            raise Exception(res["message"])

    def upload_annotation_from_cocojson(self, file_path: str):
        """
        available soon
        """
        datalake_logger.debug(f'file_name={file_path}')
        _annotation = GroundTruth(client=self)
        _annotation.upload_coco(file_path)

    def upload_modelrun_from_json(
            self,
            storage_base_path: str,
            model_id: str,
            file_path: str,
            annotation_geometry: str,
            is_normalized: bool,
            dest_project_id: str,
            version: str,
            bucket_name: str,
            upload_type: AnnotationUploadType

    ):
        datalake_logger.debug(f'upload_modelrun_from_json file_path={file_path}, '
                              f'annotation_geometry={annotation_geometry}')
        _model = ModelRun(client=self)
        if annotation_geometry == BOX_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, BOX_ANNOTATION, is_normalized, dest_project_id, version, bucket_name, upload_type)
        elif annotation_geometry == POLYGON_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, POLYGON_ANNOTATION, is_normalized, dest_project_id, version, bucket_name, upload_type)
        elif annotation_geometry == LINE_ANNOTATION:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, LINE_ANNOTATION, is_normalized, dest_project_id, version, bucket_name, upload_type)
        elif annotation_geometry is None:
            _model.upload_modelrun_json(storage_base_path, model_id, file_path, None, is_normalized, dest_project_id, version, bucket_name, upload_type)
        else:
            datalake_logger.debug(f'unsupported annotation_geometry={annotation_geometry}')

    def upload_groundtruth_from_json(
            self,
            storage_base_path: str,
            operation_id: str,
            file_path: str,
            annotation_geometry: str,
            is_normalized: bool,
            dest_project_id: str,
            version: str,
            bucket_name: str,
            upload_type: AnnotationUploadType
    ):
        datalake_logger.debug(f'upload_groundtruth_from_json file_path={file_path}, '
                              f'annotation_geometry={annotation_geometry}')
        _groundTruth = GroundTruth(client=self)
        if annotation_geometry == BOX_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, BOX_ANNOTATION, is_normalized, dest_project_id, version, bucket_name, upload_type)
        elif annotation_geometry == POLYGON_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, POLYGON_ANNOTATION, is_normalized, dest_project_id, version, bucket_name, upload_type)
        elif annotation_geometry == LINE_ANNOTATION:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, LINE_ANNOTATION, is_normalized, dest_project_id, version, bucket_name, upload_type)
        elif annotation_geometry is None:
            _groundTruth.upload_groundtruth_json(storage_base_path, operation_id, file_path, None, is_normalized, dest_project_id, version, bucket_name, upload_type)
        else:
            datalake_logger.debug(f'unsupported annotation_geometry={annotation_geometry}')

    def file_upload(self, path: str, collection_type, collection_name, meta_data_object, application_code, meta_data_override, storage_prefix_path):
        _upload = FileUpload(client=self, application_code=application_code)
        upload_res = _upload.file_upload_initiate(path, collection_type, collection_name, meta_data_object, meta_data_override, storage_prefix_path)
        return upload_res

    def get_upload_status(self, collection_name):
        _upload = FileUpload(client=self)
        return _upload.get_upload_status(collection_name)

    def remove_collection_annotations(self, collection_id: str, model_run_id: str):
        print(f'annotation delete of collection ={collection_id}', f'model id={model_run_id}')
        _model = Annotation(client=self)
        _model.remove_collection_annotations(collection_id, model_run_id)


    """
    get selection id for query, collection id, filter data
    """
    def get_selection_id(self, collection_id, query, filter, object_type, object_list, is_all_selected=True):
        _query = Query(client=self)
        response = _query.get_selection_id(collection_id, query, filter, object_type, object_list, is_all_selected)
        return response


    def get_object_type_by_id(self, object_id):
        response = self.datalake_interface.get_object_type_by_id(object_id)
        return response

    def get_system_labels(self, group_id = None):
        response = self.datalake_interface.get_all_label_list(group_id)
        return response

    def attach_labels_to_group(self, group_id, label_keys):
        if group_id == '' or len(label_keys) == 0:
            print('Label group id or label list is empty')
            return { "is_success": False}
        response = self.datalake_interface.add_labels_to_group(group_id, label_keys)
        return response

    def detach_labels_from_group(self, group_id, label_keys):
        if group_id == '' or len(label_keys) == 0:
            print('Label group id or label list is empty')
            return { "is_success": False}
        response = self.datalake_interface.remove_labels_from_group(group_id, label_keys)
        return response

    def get_all_label_groups(self):
        response = self.datalake_interface.get_all_group_list()
        return response

    def create_system_label(self, label_dict):
        _label_dict = Label.get_system_label_create_payload(label_dict)
        response = self.datalake_interface.create_system_label(_label_dict)
        if response is not None:
            response = {
                "label_reference" : response["label"]
            }
        return response


    def create_label_group(self, group_name, label_keys):
        if group_name == '' or len(label_keys) == 0:
            print('Label group name or label list is empty')
            return None
        response = self.datalake_interface.create_label_group(group_name, label_keys)
        return response

    def wait_for_job_complete(self, job_id):
        print(f"Waiting until complete the job: {job_id}")
        while True:
            try:
                job_detils = self.datalake_interface.check_job_status(job_id)

                if job_detils["isSuccess"]:
                    job_status = job_detils["status"]
                    job_progress = job_detils["progress"]
                    print(f'Job progress: {job_progress:.2f}%')
                    if job_status == JobStatus.COMPLETED.value:
                        res = {
                            "is_success" : True,
                            "job_status" : "COMPLETED"
                        }
                        print(res)
                        return res
                    elif job_status == JobStatus.FAILED.value:
                        res = {
                            "is_success" : True,
                            "job_status" : "COMPLETED"
                        }
                        print(res)
                        return res
                    else:
                        time.sleep(30)
                else:
                    res = {
                        "is_success": False,
                        "job_status": "FAILED"
                    }
                    print(res)
                    return res
            except Exception as e:
                print(f"An exception occurred: {format(e)}")
                res = {
                    "is_success": False,
                    "job_status": "FAILED"
                }
                print(res)
                return res
    
    """
    trash selection object
    """
    def trash_datalake_object(self, selection_id):
        _trash = FileTrash(client=self)
        return _trash.trash_files(selection_id)

    def get_file_download_url(self, file_key):
        return self.datalake_interface.get_file_download_url(file_key)
    
    """
    upload metadata by using json file
    """
    def upload_metadata_from_json(
            self,
            storage_base_path: str,
            object_type: str,
            file_path: str,
    ):
        _metadata = Metadata(client=self)
        response =  _metadata.upload_metadata_json(storage_base_path,object_type, file_path)
        print(response.get("message"))
        return response

    """
    upload metadata by using meta object
    """
    def upload_metadata_from_metaObject(
            self,
            collection_name: str,
            object_type: str,
            metadata_object: dict,
            is_apply_to_all_files: bool
    ):
        _metadata = Metadata(client=self)
        response = _metadata.upload_metadata_object(collection_name,object_type, metadata_object, is_apply_to_all_files)
        print(response.get("message"))
        return response
    
    """
    get item list from datalake

    """
    def get_item_list_from_datalake(
            self, 
            item_type_enum,
            query: str,
            filter = {},
            page_index = 0,
            page_size = 20
            ):
        payload = {
            "pageIndex": page_index,
            "pageSize": page_size,
            "query": query,
            "filterData": filter
        }
        item_list = self.datalake_interface.get_item_list_from_datalake(payload)

        return item_list
    
    """
    get item list from collection in datalake
    
    """
    def get_item_list_from_collection(
            self, 
            collection_id,
            query: str,
            filter = {},
            page_index = 0,
            page_size = 20
            ):
        payload = {
            "pageIndex": page_index,
            "pageSize": page_size,
            "query": query,
            "filterData": filter
        }
        item_list = self.datalake_interface.get_item_list_from_collection(payload, collection_id)

        return item_list

    """
    get metadata by using filter
    @param unique_name: unique file name
    @param filter: filter to get required meta data
    """
    def get_item_details(self, unique_name : str, filter: dict):

        if unique_name == None or unique_name == "":
            raise Exception("unique_name is empty")
        
        if filter == None:
            filter = {}

        payload = {
            "uniqueFileName": unique_name,
            "requiredMetaObj": filter 
        }

        res = self.datalake_interface.get_item_details(payload)

        if res["isSuccess"] == False:
            raise Exception(res["message"])
        else:
            return res["itemDetails"]
        
    """
    get metadata by using filter
    @param unique_file_name: unique file name
    @param filter: filter to get required meta data
    """
    def get_collection_details(self, collection_id : str, filter: dict):

        if collection_id == None or collection_id == "":
            raise Exception("collection_id is empty")
        
        if filter == None:
            filter = {}

        payload = {
            "collectionId": collection_id,
            "requiredMetaObj": filter 
        }

        res = self.datalake_interface.get_collection_details(payload)

        if res["isSuccess"] == False:
            raise Exception(res["message"])
        else:
            return res["itemDetails"]
    