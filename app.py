import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",  # Thay bằng mật khẩu của bạn
        database="quanlytourdulich"  # Thay bằng tên database của bạn
    )
    return connection
@app.route('/')
def trang_chu():
    return render_template('index.html')

@app.route('/tim-kiem-tour', methods=['GET'])
def danh_sach_tour():
    ten_tour = request.args.get('ten_tour', '')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Nếu có yêu cầu tìm kiếm, sử dụng LIKE để tìm theo tên
    if ten_tour:
        query = "SELECT * FROM Tour WHERE ten_tour LIKE %s"
        cursor.execute(query, ('%' + ten_tour + '%',))
    else:
        query = "SELECT * FROM Tour"
        cursor.execute(query)

    tours = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('list.html', tours=tours)

@app.route('/quan-ly-tour')
def quan_ly_tour():
    # Truy vấn và hiển thị danh sách tour
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Tour")
    tours = cursor.fetchall()
    
    conn.close()
    return render_template('manage_tour.html', tours=tours)
@app.route('/them-tour', methods=['GET', 'POST'])
def them_tour():
    if request.method == 'POST':
        ten_tour = request.form['ten_tour']
        noi_xuat_phat = request.form['noi_xuat_phat']
        noi_den = request.form['noi_den']
        mo_ta = request.form['mo_ta']
        ngay_xuat_phat = request.form['ngay_xuat_phat']
        gia_tour = request.form['gia_tour']
        so_luong_ve = request.form['so_luong_ve']

        # Kết nối tới cơ sở dữ liệu
        conn = get_db_connection()
        cursor = conn.cursor()

        # Chèn dữ liệu mới vào bảng Tour
        cursor.execute("""
            INSERT INTO Tour (ten_tour, noi_xuat_phat, noi_den, mo_ta, ngay_xuat_phat, gia_tour, so_luong_ve)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (ten_tour, noi_xuat_phat, noi_den, mo_ta, ngay_xuat_phat, gia_tour, so_luong_ve))

        conn.commit()
        conn.close()

        # Sau khi thêm tour thành công, chuyển hướng về trang quản lý tour
        return redirect(url_for('quan_ly_tour'))

    return render_template('add_tour.html')
@app.route('/sua-tour/<int:ma_tour>', methods=['GET', 'POST'])
def sua_tour(ma_tour):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        ten_tour = request.form['ten_tour']
        noi_xuat_phat = request.form['noi_xuat_phat']
        noi_den = request.form['noi_den']
        ngay_xuat_phat = request.form['ngay_xuat_phat']
        gia_tour = request.form['gia_tour']
        so_luong_ve = request.form['so_luong_ve']

        # Cập nhật dữ liệu tour trong database
        cursor.execute("""
            UPDATE Tour
            SET ten_tour = %s, noi_xuat_phat = %s, noi_den = %s, ngay_xuat_phat = %s, gia_tour = %s, so_luong_ve = %s
            WHERE ma_tour = %s
        """, (ten_tour, noi_xuat_phat, noi_den, ngay_xuat_phat, gia_tour, so_luong_ve, ma_tour))

        conn.commit()
        conn.close()
        return redirect(url_for('quan_ly_tour'))

    # Lấy thông tin tour hiện tại từ database
    cursor.execute("SELECT * FROM Tour WHERE ma_tour = %s", (ma_tour,))
    tour = cursor.fetchone()
    conn.close()
    
    return render_template('edit_tour.html', tour=tour)
@app.route('/xoa-tour/<int:ma_tour>', methods=['POST'])
def xoa_tour(ma_tour):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Xóa tour dựa trên mã tour
        cursor.execute("DELETE FROM Tour WHERE ma_tour = %s", (ma_tour,))
        conn.commit()
    except Exception as e:
        conn.rollback()  # Rollback nếu có lỗi
        print(f"Lỗi: {e}")
    finally:
        conn.close()  # Đóng kết nối sau khi xóa

    # Quay lại trang quản lý tour
    return redirect(url_for('quan_ly_tour'))

@app.route('/quan-ly-khach-hang')
def quan_ly_khach_hang():
    conn = get_db_connection()  # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor(dictionary=True)  # Sử dụng dictionary cursor
    
    cursor.execute("SELECT * FROM KhachHang")  # Truy vấn tất cả khách hàng
    khach_hangs = cursor.fetchall()  # Lấy danh sách khách hàng

    conn.close()  # Đóng kết nối
    
    # Truyền danh sách khách hàng vào template
    return render_template('manage_khach_hang.html', khach_hangs=khach_hangs)

@app.route('/them-khach-hang', methods=['GET', 'POST'])
def them_khach_hang():
    if request.method == 'POST':
        ten_khach_hang = request.form['ten_khach_hang']
        so_id = request.form['so_id']
        loai_id = request.form['loai_id']
        so_dien_thoai = request.form['so_dien_thoai']
        email = request.form['email']
        dia_chi = request.form['dia_chi']

        # Kết nối đến cơ sở dữ liệu
        conn = get_db_connection()
        cursor = conn.cursor()

        # Thêm khách hàng mới vào bảng KhachHang
        cursor.execute("""
            INSERT INTO KhachHang (ten_khach_hang, so_id, loai_id, so_dien_thoai, email, dia_chi)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (ten_khach_hang, so_id, loai_id, so_dien_thoai, email, dia_chi))
        
        conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        conn.close()   # Đóng kết nối

        return redirect(url_for('quan_ly_khach_hang'))  # Quay lại trang quản lý khách hàng sau khi thêm

    # Hiển thị form nếu là phương thức GET
    return render_template('them_khach_hang.html')
@app.route('/thong-ke')
def thong_ke():
    conn = get_db_connection()  # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor(dictionary=True)  # Sử dụng dictionary cursor
    
    # Thống kê tổng doanh thu
    cursor.execute("SELECT SUM(tong_tien) AS tong_doanh_thu FROM DatVe")
    tong_doanh_thu = cursor.fetchone()["tong_doanh_thu"]
    
    # Thống kê số lượng khách hàng
    cursor.execute("SELECT COUNT(ma_khach_hang) AS so_luong_khach_hang FROM KhachHang")
    so_luong_khach_hang = cursor.fetchone()["so_luong_khach_hang"]
    
    # Thống kê số lượng tour đã được đặt
    cursor.execute("SELECT COUNT(DISTINCT ma_tour) AS so_luong_tour_da_dat FROM DatVe")
    so_luong_tour_da_dat = cursor.fetchone()["so_luong_tour_da_dat"]

    conn.close()  # Đóng kết nối

    # Truyền các dữ liệu thống kê vào template
    return render_template('thong_ke.html', tong_doanh_thu=tong_doanh_thu, 
                           so_luong_khach_hang=so_luong_khach_hang, 
                           so_luong_tour_da_dat=so_luong_tour_da_dat)

@app.route('/sua-khach-hang/<int:ma_khach_hang>', methods=['GET', 'POST'])
def sua_khach_hang(ma_khach_hang):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Lấy dữ liệu từ form
        ten_khach_hang = request.form['ten_khach_hang']
        so_id = request.form['so_id']
        loai_id = request.form['loai_id']
        so_dien_thoai = request.form['so_dien_thoai']
        email = request.form['email']
        dia_chi = request.form['dia_chi']

        # Cập nhật thông tin khách hàng trong cơ sở dữ liệu
        cursor.execute("""
            UPDATE KhachHang 
            SET ten_khach_hang = %s, so_id = %s, loai_id = %s, so_dien_thoai = %s, email = %s, dia_chi = %s
            WHERE ma_khach_hang = %s
        """, (ten_khach_hang, so_id, loai_id, so_dien_thoai, email, dia_chi, ma_khach_hang))

        conn.commit()
        conn.close()

        return redirect(url_for('quan_ly_khach_hang'))  # Quay lại trang quản lý khách hàng sau khi sửa

    # Lấy thông tin khách hàng hiện tại để hiển thị trong form
    cursor.execute("SELECT * FROM KhachHang WHERE ma_khach_hang = %s", (ma_khach_hang,))
    khach_hang = cursor.fetchone()

    conn.close()

    return render_template('sua_khach_hang.html', khach_hang=khach_hang)

if __name__ == '__main__':
    app.run(debug=True)
