// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//         http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

const py = @import("./pydust.zig");
const tramp = @import("./trampoline.zig");

/// Zig PyObject-like -> ffi.PyObject. Convert a Zig PyObject-like value into a py.PyObject.
///  e.g. py.PyObject, py.PyTuple, ffi.PyObject, etc.
pub inline fn object(value: anytype) py.PyObject {
    return tramp.Trampoline(@TypeOf(value)).asObject(value);
}

/// Zig -> Python. Return a Python representation of a Zig object.
/// For Zig primitives, this constructs a new Python object.
/// For PyObject-like values, this returns the value without creating a new reference.
pub inline fn createOwned(value: anytype) py.PyError!py.PyObject {
    const trampoline = tramp.Trampoline(@TypeOf(value));
    defer trampoline.decref_objectlike(value);
    return trampoline.wrap(value);
}

/// Zig -> Python. Convert a Zig object into a Python object. Returns a new object.
pub inline fn create(value: anytype) py.PyError!py.PyObject {
    return tramp.Trampoline(@TypeOf(value)).wrap(value);
}

/// Python -> Zig. Return a Zig object representing the Python object.
pub inline fn as(comptime T: type, obj: anytype) py.PyError!T {
    return tramp.Trampoline(T).unwrap(object(obj));
}

const testing = @import("std").testing;
const expect = testing.expect;

test "as py -> zig" {
    py.initialize();
    defer py.finalize();

    // Start with a Python object
    const str = try py.PyString.create("hello");
    try expect(py.refcnt(str) == 1);

    // Return a slice representation of it, and ensure the refcnt is untouched
    _ = try py.as([]const u8, str);
    try expect(py.refcnt(str) == 1);

    // Return a PyObject representation of it, and ensure the refcnt is untouched.
    _ = try py.as(py.PyObject, str);
    try expect(py.refcnt(str) == 1);
}

test "create" {
    py.initialize();
    defer py.finalize();

    const str = try py.PyString.create("Hello");
    try testing.expectEqual(@as(isize, 1), py.refcnt(str));

    const some_tuple = try py.create(.{str});
    defer some_tuple.decref();
    try testing.expectEqual(@as(isize, 2), py.refcnt(str));

    str.decref();
    try testing.expectEqual(@as(isize, 1), py.refcnt(str));
}

test "createOwned" {
    py.initialize();
    defer py.finalize();

    const str = try py.PyString.create("Hello");
    try testing.expectEqual(@as(isize, 1), py.refcnt(str));

    const some_tuple = try py.createOwned(.{str});
    defer some_tuple.decref();
    try testing.expectEqual(@as(isize, 1), py.refcnt(str));
}
