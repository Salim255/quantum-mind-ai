export interface ApiResponseDTO<T> {

    status: 'success' | 'error';

    data: T;

}
